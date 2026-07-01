import os
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkfont
from pydantic import BaseModel, Field
import google.genai as genai
from google.genai import types

# Define default API Key from the workspace as default fallback
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "AIzaSyDtyi49ASpcZNdi3RR59Sck1X2GPWYgHS0"

# ==========================================
# PYDANTIC SCHEMA FOR STRUCTURED OUTPUT
# ==========================================
class PracticeQuestion(BaseModel):
    question: str = Field(description="A challenging practice question testing conceptual depth.")
    answer: str = Field(description="A detailed correct answer with explanation and shortcuts.")

class DayPlan(BaseModel):
    day: int = Field(description="The day number (1-indexed).")
    title: str = Field(description="Main focus of this day's revision.")
    key_topics: list[str] = Field(description="Core subtopics to cover on this day.")
    revision_bits: list[str] = Field(description="Concise, high-yield bullet notes, concepts, and NCERT-based core fundamentals.")
    formulas_or_key_terms: list[str] = Field(description="Crucial formulas (ASCII text format) or key glossary definitions.")
    exam_tips: list[str] = Field(description="Traps, common mistakes, Board/JEE/NEET scoring tips, or NCERT specific caveats.")
    practice_questions: list[PracticeQuestion] = Field(description="Exactly 3 practice questions with detailed answers.")

class RevisionPlanSchema(BaseModel):
    subject: str = Field(description="Subject name.")
    topic: str = Field(description="The revised topic.")
    target_class: str = Field(description="Targeted competitive exam or class standard.")
    days: list[DayPlan] = Field(description="Daily revision plan, exactly matching the requested duration.")


# ==========================================
# CUSTOM SCROLLABLE FRAME WIDGET
# ==========================================
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg="#0f172a", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=bg)
        
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Dynamic scroll binding on mouse hover
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ==========================================
# CUSTOM PROGRESS BAR
# ==========================================
class ModernProgressBar(tk.Canvas):
    def __init__(self, parent, bg="#1e293b", height=10, *args, **kwargs):
        super().__init__(parent, bg=bg, highlightthickness=0, height=height, *args, **kwargs)
        self.progress = 0.0
        self.bind("<Configure>", lambda e: self.draw())
        
    def set_progress(self, progress):
        self.progress = max(0.0, min(1.0, progress))
        self.draw()
        
    def draw(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1:
            return
            
        # Draw background bar
        self.create_rectangle(0, 0, width, height, fill="#1e293b", width=0)
        # Draw progress bar fill
        fill_width = int(width * self.progress)
        if fill_width > 0:
            self.create_rectangle(0, 0, fill_width, height, fill="#14b8a6", width=0)


# ==========================================
# AUTO WRAP LABEL HELPER
# ==========================================
class AutoWrapLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        # Dynamically adjust wraplength based on parent frame's configuration
        padding = 40
        self.configure(wraplength=max(100, event.width - padding))


# ==========================================
# MAIN APPLICATION CLASS
# ==========================================
class RevisionIOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RevisionIO - Competitive Exam Revision Planner")
        self.root.geometry("1150x780")
        self.root.minsize(1000, 680)
        
        # Set dark-mode base color system
        self.colors = {
            "bg_main": "#0f172a",      # Slate 900
            "bg_card": "#1e293b",      # Slate 800
            "fg_bright": "#f8fafc",    # Slate 50
            "fg_muted": "#94a3b8",     # Slate 400
            "accent_indigo": "#6366f1",# Indigo 500
            "accent_indigo_hover": "#4f46e5",
            "accent_teal": "#14b8a6",  # Teal 500
            "border": "#334155"        # Slate 700
        }
        
        # Load fonts
        available_fonts = tkfont.families()
        self.font_family = "Segoe UI" if "Segoe UI" in available_fonts else "Helvetica"
        
        # Set root style
        self.root.config(bg=self.colors["bg_main"])
        
        # Config options style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", 
                             fieldbackground=self.colors["bg_main"], 
                             background=self.colors["bg_card"], 
                             foreground=self.colors["fg_bright"], 
                             bordercolor=self.colors["border"],
                             arrowcolor=self.colors["fg_bright"])
        
        # Application State
        self.current_plan = None
        self.completed_days = {}
        self.current_viewing_day = 1
        self.answer_visibility = {} # maps (day_num, q_idx) -> bool
        
        self.build_ui()
        
    def build_ui(self):
        # 1. Outer Container Frame
        self.main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_container.pack(fill="both", expand=True)
        
        # 2. Left Sidebar (330px width)
        self.sidebar = tk.Frame(self.main_container, bg=self.colors["bg_card"], width=330)
        self.sidebar.pack(side="left", fill="y", padx=(0, 2))
        self.sidebar.pack_propagate(False) # Keep fixed width
        
        # 3. Main Dashboard Area
        self.main_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        self.setup_sidebar()
        self.setup_empty_state()

    # ==========================================
    # SIDEBAR SETUP (INPUT MODULES)
    # ==========================================
    def setup_sidebar(self):
        # Header banner
        header_frame = tk.Frame(self.sidebar, bg=self.colors["bg_card"])
        header_frame.pack(fill="x", padx=20, pady=25)
        
        lbl_logo = tk.Label(header_frame, text="RevisionIO ⚡", font=(self.font_family, 20, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_logo.pack(anchor="w")
        
        lbl_sub = tk.Label(header_frame, text="Competitive Exam Revision Planner\nBased on NCERT Syllabus", font=(self.font_family, 9, "bold"), fg=self.colors["accent_teal"], bg=self.colors["bg_card"], justify="left")
        lbl_sub.pack(anchor="w", pady=(2, 0))
        
        divider = tk.Frame(self.sidebar, bg=self.colors["border"], height=1)
        divider.pack(fill="x", padx=20, pady=(0, 15))
        
        # Scrollable panel in sidebar (incase layout overflows on small heights)
        sb_scroll = ScrollableFrame(self.sidebar, bg=self.colors["bg_card"])
        sb_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        form_frame = sb_scroll.scrollable_frame
        
        # Form field definitions
        # 1. Combobox for exam targets
        lbl_exam = tk.Label(form_frame, text="Target Examination / Standard", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_exam.pack(anchor="w", padx=15, pady=(10, 5))
        
        exam_options = [
            "JEE Main (PCM)",
            "JEE Advanced (PCM)",
            "NEET Prep (PCB)",
            "CUET Science (PCM/PCB)",
            "CUET Commerce (Accountancy/BST/Economics)",
            "CBSE Class 12 Boards + Competitive",
            "CBSE Class 11 Boards + Competitive",
            "CBSE Class 10 Boards + NTSE Foundation",
            "CBSE Class 9 Boards + Olympiad Prep",
            "Olympiad Foundation (Classes 6-8)"
        ]
        self.class_combobox = ttk.Combobox(form_frame, values=exam_options, state="readonly", font=(self.font_family, 10))
        self.class_combobox.set(exam_options[0])
        self.class_combobox.pack(fill="x", padx=15, pady=(0, 15))
        
        # 2. Subject Input
        lbl_subj = tk.Label(form_frame, text="Subject", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_subj.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.subject_border, self.subject_entry = self.create_flat_entry(form_frame, placeholder="e.g. Physics")
        self.subject_border.pack(fill="x", padx=15, pady=(0, 15))
        
        # 3. Topic Input
        lbl_topic = tk.Label(form_frame, text="Topic to Revise", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_topic.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.topic_border, self.topic_entry = self.create_flat_entry(form_frame, placeholder="e.g. Electrostatics")
        self.topic_border.pack(fill="x", padx=15, pady=(0, 15))
        
        # 4. Days Scale
        lbl_days = tk.Label(form_frame, text="Revision Period (Days)", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_days.pack(anchor="w", padx=15, pady=(0, 2))
        
        self.days_slider = tk.Scale(
            form_frame,
            from_=1, to=15,
            orient="horizontal",
            bg=self.colors["bg_card"],
            fg=self.colors["fg_bright"],
            troughcolor=self.colors["bg_main"],
            activebackground=self.colors["accent_indigo"],
            highlightthickness=0,
            font=(self.font_family, 9),
            bd=0
        )
        self.days_slider.set(5)
        self.days_slider.pack(fill="x", padx=15, pady=(0, 15))
        
        # 5. Dedicated Hours Scale
        lbl_hours = tk.Label(form_frame, text="Daily Study Commitment (Hours)", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_hours.pack(anchor="w", padx=15, pady=(0, 2))
        
        self.hours_slider = tk.Scale(
            form_frame,
            from_=1, to=12,
            orient="horizontal",
            bg=self.colors["bg_card"],
            fg=self.colors["fg_bright"],
            troughcolor=self.colors["bg_main"],
            activebackground=self.colors["accent_indigo"],
            highlightthickness=0,
            font=(self.font_family, 9),
            bd=0
        )
        self.hours_slider.set(3)
        self.hours_slider.pack(fill="x", padx=15, pady=(0, 15))
        
        # 6. API Key Input
        lbl_key = tk.Label(form_frame, text="Gemini API Key", font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_key.pack(anchor="w", padx=15, pady=(0, 5))
        
        key_container = tk.Frame(form_frame, bg=self.colors["bg_card"])
        key_container.pack(fill="x", padx=15, pady=(0, 20))
        
        self.key_border, self.api_key_entry = self.create_flat_entry(key_container, show="*")
        self.key_border.pack(side="left", fill="x", expand=True)
        self.api_key_entry.insert(0, DEFAULT_API_KEY)
        
        # Toggle view key button
        self.show_key_var = tk.BooleanVar(value=False)
        self.btn_toggle_key = tk.Button(
            key_container,
            text="👁️",
            command=self.toggle_api_key_visibility,
            bg=self.colors["bg_card"],
            fg=self.colors["fg_muted"],
            activebackground=self.colors["bg_card"],
            activeforeground=self.colors["fg_bright"],
            relief="flat",
            bd=0,
            font=(self.font_family, 11),
            cursor="hand2"
        )
        self.btn_toggle_key.pack(side="right", padx=(5, 0))
        
        # 7. Action Button: Generate
        self.btn_generate = self.create_flat_button(
            form_frame,
            text="Generate Revision Plan ✨",
            command=self.start_generation,
            bg=self.colors["accent_indigo"],
            activebg=self.colors["accent_indigo_hover"]
        )
        self.btn_generate.pack(fill="x", padx=15, pady=(10, 15))
        
        # Divider before persistence buttons
        sub_divider = tk.Frame(form_frame, bg=self.colors["border"], height=1)
        sub_divider.pack(fill="x", padx=15, pady=(5, 15))
        
        # Persistence Frame (Save/Load)
        persist_frame = tk.Frame(form_frame, bg=self.colors["bg_card"])
        persist_frame.pack(fill="x", padx=15, pady=(0, 20))
        
        self.btn_save = self.create_flat_button(
            persist_frame,
            text="Save Plan 💾",
            command=self.save_plan,
            bg="#334155",
            activebg="#475569",
            font=(self.font_family, 10, "bold")
        )
        self.btn_save.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_load = self.create_flat_button(
            persist_frame,
            text="Load Plan 📂",
            command=self.load_plan,
            bg="#334155",
            activebg="#475569",
            font=(self.font_family, 10, "bold")
        )
        self.btn_load.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
    def create_flat_entry(self, parent, show=None, placeholder=""):
        border_frame = tk.Frame(parent, bg=self.colors["border"], bd=1)
        entry = tk.Entry(
            border_frame,
            bg=self.colors["bg_main"],
            fg=self.colors["fg_bright"],
            insertbackground=self.colors["fg_bright"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=(self.font_family, 10),
            show=show
        )
        entry.pack(fill="both", expand=True, padx=8, pady=6)
        
        # Dynamic focus ring
        def on_focus_in(e):
            border_frame.config(bg=self.colors["accent_indigo"])
        def on_focus_out(e):
            border_frame.config(bg=self.colors["border"])
            
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        return border_frame, entry

    def create_flat_button(self, parent, text, command, bg="#4f46e5", activebg="#4338ca", font=None):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.colors["fg_bright"],
            activebackground=activebg,
            activeforeground=self.colors["fg_bright"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=font or (self.font_family, 11, "bold"),
            cursor="hand2",
            padx=10,
            pady=8
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=activebg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def toggle_api_key_visibility(self):
        show_key = not self.show_key_var.get()
        self.show_key_var.set(show_key)
        if show_key:
            self.api_key_entry.config(show="")
            self.btn_toggle_key.config(text="🙈", fg=self.colors["fg_bright"])
        else:
            self.api_key_entry.config(show="*")
            self.btn_toggle_key.config(text="👁️", fg=self.colors["fg_muted"])

    # ==========================================
    # EMPTY STATE UI
    # ==========================================
    def setup_empty_state(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        empty_container = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        empty_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Banner/Icon
        lbl_icon = tk.Label(empty_container, text="⚡📖⚡", font=(self.font_family, 36), fg=self.colors["accent_indigo"], bg=self.colors["bg_main"])
        lbl_icon.pack(pady=10)
        
        lbl_title = tk.Label(empty_container, text="No Revision Plan Loaded", font=(self.font_family, 18, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_main"])
        lbl_title.pack(pady=5)
        
        lbl_desc = tk.Label(
            empty_container,
            text="Configure your target exam, subject, and topic on the left sidebar, then click 'Generate' to create a comprehensive day-wise revision roadmap matching the NCERT syllabus and competitive standard.\n\nYou can also reload a previously saved plan using the 'Load Plan' button.",
            font=(self.font_family, 10),
            fg=self.colors["fg_muted"],
            bg=self.colors["bg_main"],
            wraplength=450,
            justify="center"
        )
        lbl_desc.pack(pady=10)

    # ==========================================
    # ASYNCHRONOUS GENERATION SYSTEM
    # ==========================================
    def start_generation(self):
        subject = self.subject_entry.get().strip()
        topic = self.topic_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        
        if not subject:
            messagebox.showwarning("Input Error", "Please specify a Subject (e.g. Physics, Chemistry, Mathematics).")
            return
        if not topic:
            messagebox.showwarning("Input Error", "Please enter the Topic you wish to revise.")
            return
        if not api_key:
            messagebox.showwarning("API Key Error", "Please provide a valid Gemini API Key to run the backend.")
            return
            
        days = int(self.days_slider.get())
        hours = int(self.hours_slider.get())
        target_class = self.class_combobox.get()
        
        # Display Loading Screen Overlay
        self.show_loading_screen(f"Curating a tailored {days}-day plan for '{topic}' ({subject}) optimized for {target_class} and NCERT core...")
        
        # Disable sidebar triggers to prevent duplicate thread starts
        self.set_sidebar_state("disabled")
        
        # Launch thread
        generation_thread = threading.Thread(
            target=self.run_gemini_backend,
            args=(api_key, target_class, subject, topic, days, hours),
            daemon=True
        )
        generation_thread.start()
        
    def show_loading_screen(self, desc_text):
        self.loading_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        box = tk.Frame(self.loading_frame, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        box.place(relx=0.5, rely=0.5, anchor="center", width=480, height=260)
        
        self.loading_icon = tk.Label(box, text="⚡", font=(self.font_family, 38), fg=self.colors["accent_teal"], bg=self.colors["bg_card"])
        self.loading_icon.pack(pady=(45, 10))
        
        self.loading_title = tk.Label(box, text="Generating Revision Plan...", font=(self.font_family, 15, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        self.loading_title.pack(pady=5)
        
        loading_desc = tk.Label(box, text=desc_text, font=(self.font_family, 9), fg=self.colors["fg_muted"], bg=self.colors["bg_card"], wraplength=420, justify="center")
        loading_desc.pack(pady=5)
        
        self.animation_step = 0
        self.animate_loading()
        
    def animate_loading(self):
        if hasattr(self, "loading_frame") and self.loading_frame.winfo_exists():
            self.animation_step = (self.animation_step + 1) % 4
            dots = "." * self.animation_step
            self.loading_title.config(text=f"Generating Revision Plan{dots}")
            
            # Pulse colors on lightning icon
            pulse_colors = [self.colors["accent_teal"], self.colors["accent_indigo"], "#f59e0b", "#3b82f6"]
            self.loading_icon.config(fg=pulse_colors[self.animation_step])
            self.root.after(450, self.animate_loading)
            
    def hide_loading_screen(self):
        if hasattr(self, "loading_frame") and self.loading_frame.winfo_exists():
            self.loading_frame.destroy()
            
    def set_sidebar_state(self, state):
        self.class_combobox.config(state=state if state == "disabled" else "readonly")
        self.subject_entry.config(state=state)
        self.topic_entry.config(state=state)
        self.days_slider.config(state=state)
        self.hours_slider.config(state=state)
        self.api_key_entry.config(state=state)
        self.btn_generate.config(state=state)
        self.btn_load.config(state=state)
        self.btn_save.config(state=state)
        
    def run_gemini_backend(self, api_key, target_class, subject, topic, days, hours):
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            You are a premier senior IIT/NEET faculty member and academic revision architect.
            The student is preparing for the competitive exam / standard: {target_class}.
            The subject is: {subject}.
            The topic to revise: {topic}.
            The total revision window: {days} days.
            Student dedicates {hours} hours daily for this topic.

            Generate a highly structured, day-by-day revision syllabus matching the NCERT syllabus as the primary base, enhanced for competitive standards (detailed conceptual shortcuts, vital formulas, exam pitfalls, and standard high-yield questions).
            Each day must cover a sensible and distinct chunk that can be fully reviewed in {hours} hours.
            Make sure the mathematical formulas are clearly rendered in readable plain ASCII.
            You must output exactly {days} days in the JSON array.
            
            Return the output strictly in JSON format matching the schema.
            """
            
            # Using model gemini-2.5-flash as standard for high speed and reliable structure output
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RevisionPlanSchema,
                    temperature=0.65
                )
            )
            
            raw_text = response.text
            plan_dict = json.loads(raw_text)
            
            # Dispatch back to Tkinter main thread
            self.root.after(0, self.on_generation_success, plan_dict)
            
        except Exception as e:
            self.root.after(0, self.on_generation_failure, str(e))
            
    def on_generation_success(self, plan_data):
        self.hide_loading_screen()
        self.set_sidebar_state("normal")
        self.current_plan = plan_data
        
        # Reset state parameters
        self.completed_days = {d["day"]: False for d in plan_data["days"]}
        self.current_viewing_day = 1
        self.answer_visibility.clear()
        
        self.render_plan_dashboard()
        
    def on_generation_failure(self, error_msg):
        self.hide_loading_screen()
        self.set_sidebar_state("normal")
        messagebox.showerror("Gemini Engine Error", f"Failed to generate revision details from Gemini API.\n\nDetails:\n{error_msg}")

    # ==========================================
    # DASHBOARD RENDERING SYSTEM
    # ==========================================
    def render_plan_dashboard(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        if not self.current_plan:
            self.setup_empty_state()
            return
            
        # Parent layout inside main frame
        # Row 0: Dashboard Header Card
        # Row 1: Navigation & Progress control bar
        # Row 2: Scrollable Day Content Frame
        
        # 1. Header Card
        header_card = tk.Frame(self.main_frame, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        header_card.pack(fill="x", padx=20, pady=(15, 10))
        
        title_text = f"Revision Plan: {self.current_plan.get('topic', 'N/A')}"
        lbl_p_title = tk.Label(header_card, text=title_text, font=(self.font_family, 16, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_p_title.pack(anchor="w", padx=20, pady=(15, 2))
        
        meta_text = f"Subject: {self.current_plan.get('subject', 'N/A')}  |  Target: {self.current_plan.get('target_class', 'N/A')}  |  Window: {len(self.current_plan['days'])} Days (Study Budget: {self.hours_slider.get()} hrs/day)"
        lbl_p_meta = tk.Label(header_card, text=meta_text, font=(self.font_family, 9, "bold"), fg=self.colors["accent_teal"], bg=self.colors["bg_card"])
        lbl_p_meta.pack(anchor="w", padx=20, pady=(0, 15))
        
        # 2. Progress & Navigation Panel
        self.nav_panel = tk.Frame(self.main_frame, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        self.nav_panel.pack(fill="x", padx=20, pady=(0, 10))
        
        # Inner layout columns
        # Left side: Previous/Next buttons, Day scale slider
        nav_buttons_frame = tk.Frame(self.nav_panel, bg=self.colors["bg_card"])
        nav_buttons_frame.pack(side="left", padx=15, pady=10, fill="x", expand=True)
        
        self.btn_prev = self.create_flat_button(
            nav_buttons_frame,
            text="◀",
            command=self.prev_day,
            bg="#334155",
            activebg="#475569",
            font=(self.font_family, 11)
        )
        self.btn_prev.pack(side="left", padx=(0, 10))
        
        # Day Scale Slider
        days_count = len(self.current_plan["days"])
        self.day_scale = tk.Scale(
            nav_buttons_frame,
            from_=1, to=days_count,
            orient="horizontal",
            bg=self.colors["bg_card"],
            fg=self.colors["fg_bright"],
            troughcolor=self.colors["bg_main"],
            activebackground=self.colors["accent_indigo"],
            highlightthickness=0,
            font=(self.font_family, 9, "bold"),
            bd=0,
            command=self.on_slider_change,
            showvalue=True
        )
        self.day_scale.set(self.current_viewing_day)
        self.day_scale.pack(side="left", fill="x", expand=True, padx=10)
        
        self.btn_next = self.create_flat_button(
            nav_buttons_frame,
            text="▶",
            command=self.next_day,
            bg="#334155",
            activebg="#475569",
            font=(self.font_family, 11)
        )
        self.btn_next.pack(side="left", padx=(10, 0))
        
        # Right side: Completion checkbox & Overall Progress Bar
        self.progress_frame = tk.Frame(self.nav_panel, bg=self.colors["bg_card"])
        self.progress_frame.pack(side="right", padx=20, pady=10)
        
        # Checkbox variable
        self.completion_var = tk.BooleanVar()
        self.completion_check = tk.Checkbutton(
            self.progress_frame,
            text="Mark Day as Completed",
            variable=self.completion_var,
            command=self.toggle_day_completion,
            bg=self.colors["bg_card"],
            fg=self.colors["accent_teal"],
            selectcolor=self.colors["bg_main"],
            activebackground=self.colors["bg_card"],
            activeforeground=self.colors["accent_teal"],
            font=(self.font_family, 10, "bold"),
            cursor="hand2"
        )
        self.completion_check.pack(anchor="e", pady=(0, 4))
        
        # Progress label
        self.lbl_progress_percent = tk.Label(self.progress_frame, text="Progress: 0%", font=(self.font_family, 9, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        self.lbl_progress_percent.pack(anchor="e")
        
        self.progress_bar = ModernProgressBar(self.progress_frame, width=180, height=8)
        self.progress_bar.pack(anchor="e", pady=(2, 0))
        
        # 3. Content Scroll Frame
        self.content_scroll = ScrollableFrame(self.main_frame, bg=self.colors["bg_main"])
        self.content_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Initial Render
        self.update_progress_display()
        self.render_day_content(self.current_viewing_day)

    def on_slider_change(self, val):
        day_num = int(val)
        if day_num != self.current_viewing_day:
            self.current_viewing_day = day_num
            self.render_day_content(self.current_viewing_day)

    def prev_day(self):
        if self.current_viewing_day > 1:
            self.current_viewing_day -= 1
            self.day_scale.set(self.current_viewing_day)

    def next_day(self):
        days_count = len(self.current_plan["days"])
        if self.current_viewing_day < days_count:
            self.current_viewing_day += 1
            self.day_scale.set(self.current_viewing_day)

    def toggle_day_completion(self):
        is_completed = self.completion_var.get()
        self.completed_days[self.current_viewing_day] = is_completed
        self.update_progress_display()
        
        # Check if all completed (celebration trigger)
        if all(self.completed_days.values()):
            self.show_celebration_popup()

    def update_progress_display(self):
        total = len(self.completed_days)
        if total == 0:
            return
        completed = sum(1 for val in self.completed_days.values() if val)
        fraction = completed / total
        percent = int(fraction * 100)
        
        self.lbl_progress_percent.config(text=f"Completed: {completed}/{total} Days ({percent}%)")
        self.progress_bar.set_progress(fraction)
        
        # Update checkbox checked state for current viewing day
        self.completion_var.set(self.completed_days.get(self.current_viewing_day, False))

    def show_celebration_popup(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Congratulations!")
        dialog.geometry("450x230")
        dialog.resizable(False, False)
        dialog.config(bg=self.colors["bg_card"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center of root window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        dlg_w, dlg_h = 450, 230
        dialog.geometry(f"{dlg_w}x{dlg_h}+{root_x + (root_w - dlg_w)//2}+{root_y + (root_h - dlg_h)//2}")
        
        lbl_emoji = tk.Label(dialog, text="🏆🎉🎓", font=(self.font_family, 28), fg=self.colors["accent_teal"], bg=self.colors["bg_card"])
        lbl_emoji.pack(pady=(25, 5))
        
        lbl_congrats = tk.Label(dialog, text="Revision Completed!", font=(self.font_family, 16, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_congrats.pack(pady=5)
        
        topic_name = self.current_plan.get("topic", "the topic")
        lbl_msg = tk.Label(
            dialog,
            text=f"Outstanding work! You have successfully revised all modules for '{topic_name}'. You are now fully primed for your examinations. Keep up the high standard!",
            font=(self.font_family, 9),
            fg=self.colors["fg_muted"],
            bg=self.colors["bg_card"],
            wraplength=400,
            justify="center"
        )
        lbl_msg.pack(pady=(5, 15))
        
        btn_ok = self.create_flat_button(
            dialog,
            text="Close & Continue",
            command=dialog.destroy,
            bg=self.colors["accent_teal"],
            activebg="#0d9488",
            font=(self.font_family, 10, "bold")
        )
        btn_ok.pack(pady=(0, 20))

    # ==========================================
    # DAY CONTENT RENDERING
    # ==========================================
    def render_day_content(self, day_num):
        # Clear inner scrollable frame content
        container = self.content_scroll.scrollable_frame
        for widget in container.winfo_children():
            widget.destroy()
            
        # Get target day data
        day_data = next((d for d in self.current_plan["days"] if d["day"] == day_num), None)
        if not day_data:
            return
            
        # Sync completion checkbox
        self.completion_var.set(self.completed_days.get(day_num, False))
        
        # 1. Main day header card
        header_frame = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        header_frame.pack(fill="x", padx=10, pady=(10, 15))
        
        lbl_day = tk.Label(header_frame, text=f"DAY {day_num} FOCUS", font=(self.font_family, 11, "bold"), fg=self.colors["accent_teal"], bg=self.colors["bg_card"])
        lbl_day.pack(anchor="w", padx=15, pady=(15, 2))
        
        lbl_title = AutoWrapLabel(header_frame, text=day_data.get("title", ""), font=(self.font_family, 15, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"], justify="left")
        lbl_title.pack(anchor="w", padx=15, pady=(0, 15))
        
        # 2. Key Topics block
        topics_card = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        topics_card.pack(fill="x", padx=10, pady=(0, 15))
        self.render_card_left_border(topics_card, self.colors["accent_indigo"])
        
        topics_body = tk.Frame(topics_card, bg=self.colors["bg_card"])
        topics_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_topics_title = tk.Label(topics_body, text="🎯 Core Subtopics to Cover", font=(self.font_family, 11, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_topics_title.pack(anchor="w", pady=(0, 8))
        
        for topic in day_data.get("key_topics", []):
            lbl_bullet = AutoWrapLabel(topics_body, text=f"•  {topic}", font=(self.font_family, 10), fg=self.colors["fg_muted"], bg=self.colors["bg_card"], justify="left")
            lbl_bullet.pack(anchor="w", pady=2)
            
        # 3. Revision Bits block
        bits_card = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        bits_card.pack(fill="x", padx=10, pady=(0, 15))
        self.render_card_left_border(bits_card, self.colors["accent_teal"])
        
        bits_body = tk.Frame(bits_card, bg=self.colors["bg_card"])
        bits_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_bits_title = tk.Label(bits_body, text="💡 Revision Bits (High-Yield Concept Notes)", font=(self.font_family, 11, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_bits_title.pack(anchor="w", pady=(0, 8))
        
        for bit in day_data.get("revision_bits", []):
            lbl_bullet = AutoWrapLabel(bits_body, text=f"✦  {bit}", font=(self.font_family, 10), fg=self.colors["fg_bright"], bg=self.colors["bg_card"], justify="left")
            lbl_bullet.pack(anchor="w", pady=5)
            
        # 4. Formulas & Core terms
        formula_card = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        formula_card.pack(fill="x", padx=10, pady=(0, 15))
        self.render_card_left_border(formula_card, "#f59e0b") # Orange border
        
        formula_body = tk.Frame(formula_card, bg=self.colors["bg_card"])
        formula_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_form_title = tk.Label(formula_body, text="📝 Crucial Formulas & Glossaries", font=(self.font_family, 11, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_form_title.pack(anchor="w", pady=(0, 8))
        
        for form in day_data.get("formulas_or_key_terms", []):
            f_box = tk.Frame(formula_body, bg=self.colors["bg_main"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
            f_box.pack(fill="x", pady=4)
            lbl_formula = AutoWrapLabel(f_box, text=form, font=("Consolas", 10, "italic"), fg="#facc15", bg=self.colors["bg_main"], justify="left")
            lbl_formula.pack(anchor="w", padx=10, pady=8)
            
        # 5. Exam tips block
        tips_card = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        tips_card.pack(fill="x", padx=10, pady=(0, 15))
        self.render_card_left_border(tips_card, "#ec4899") # Pink accent
        
        tips_body = tk.Frame(tips_card, bg=self.colors["bg_card"])
        tips_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        lbl_tips_title = tk.Label(tips_body, text="⚠️ Competitive Exam Traps & NCERT Core Guidance", font=(self.font_family, 11, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"])
        lbl_tips_title.pack(anchor="w", pady=(0, 8))
        
        for tip in day_data.get("exam_tips", []):
            lbl_bullet = AutoWrapLabel(tips_body, text=f"•  {tip}", font=(self.font_family, 10), fg="#f43f5e", bg=self.colors["bg_card"], justify="left")
            lbl_bullet.pack(anchor="w", pady=4)
            
        # 6. Self Test Section
        lbl_sect_quiz = tk.Label(container, text="🔥 Practice Challenges (Reveal Answer)", font=(self.font_family, 12, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_main"])
        lbl_sect_quiz.pack(anchor="w", padx=10, pady=(5, 10))
        
        questions = day_data.get("practice_questions", [])
        for idx, q_item in enumerate(questions):
            q_card = tk.Frame(container, bg=self.colors["bg_card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
            q_card.pack(fill="x", padx=10, pady=(0, 12))
            self.render_card_left_border(q_card, self.colors["accent_teal"])
            
            q_body = tk.Frame(q_card, bg=self.colors["bg_card"])
            q_body.pack(fill="both", expand=True, padx=15, pady=15)
            
            # Question Header
            lbl_q_head = tk.Label(q_body, text=f"Practice Problem {idx + 1}", font=(self.font_family, 10, "bold"), fg=self.colors["accent_teal"], bg=self.colors["bg_card"])
            lbl_q_head.pack(anchor="w", pady=(0, 2))
            
            lbl_question = AutoWrapLabel(q_body, text=q_item.get("question", ""), font=(self.font_family, 10, "bold"), fg=self.colors["fg_bright"], bg=self.colors["bg_card"], justify="left")
            lbl_question.pack(anchor="w", pady=(0, 10))
            
            # Answer Toggle Container
            ans_key = (day_num, idx)
            is_visible = self.answer_visibility.get(ans_key, False)
            
            # Hidden Answer frame
            ans_frame = tk.Frame(q_body, bg=self.colors["bg_main"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
            lbl_ans = AutoWrapLabel(ans_frame, text=f"Solution:\n{q_item.get('answer', '')}", font=(self.font_family, 9.5), fg="#34d399", bg=self.colors["bg_main"], justify="left")
            lbl_ans.pack(fill="x", padx=12, pady=10)
            
            if is_visible:
                ans_frame.pack(fill="x", pady=(0, 5))
                btn_txt = "Hide Detailed Solution 🙈"
            else:
                btn_txt = "Reveal Solution 👁️"
                
            def make_toggle_cmd(k=ans_key, f=ans_frame, a_item=q_item):
                return lambda: self.toggle_answer_visibility(k, f)
                
            btn_reveal = self.create_flat_button(
                q_body,
                text=btn_txt,
                command=make_toggle_cmd(),
                bg="#334155",
                activebg="#475569",
                font=(self.font_family, 9, "bold")
            )
            btn_reveal.pack(anchor="w", pady=(5, 5))
            
            q_body.btn_reference = btn_reveal
            
    def render_card_left_border(self, card, border_color):
        border = tk.Frame(card, bg=border_color, width=4)
        border.pack(side="left", fill="y")

    def toggle_answer_visibility(self, ans_key, ans_frame):
        current_state = self.answer_visibility.get(ans_key, False)
        new_state = not current_state
        self.answer_visibility[ans_key] = new_state
        self.render_day_content(self.current_viewing_day)

    # ==========================================
    # FILE PERSISTENCE ENGINE
    # ==========================================
    def save_plan(self):
        if not self.current_plan:
            messagebox.showwarning("Save Plan", "No plan active to save. Please generate a revision roadmap first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("RevisionIO Plans", "*.json")],
            title="Save Revision Roadmap",
            initialfile=f"{self.current_plan.get('topic', 'Revision')}_Plan.json"
        )
        if not file_path:
            return
            
        packaged_data = {
            "plan": self.current_plan,
            "completed_days": self.completed_days,
            "view_day": self.current_viewing_day
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(packaged_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Save Successful", f"Your revision plan has been successfully written to:\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Save File Error", f"Failed to save plan on system disk.\n\nError: {e}")

    def load_plan(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("RevisionIO Plans", "*.json")],
            title="Open Revision Roadmap"
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                packaged_data = json.load(f)
                
            if "plan" in packaged_data and "completed_days" in packaged_data:
                self.current_plan = packaged_data["plan"]
                
                # Convert loaded keys back to integer values (JSON requires string keys)
                loaded_completes = packaged_data["completed_days"]
                self.completed_days = {int(day): bool(status) for day, status in loaded_completes.items()}
                
                # Retrieve viewing day or fallback to 1
                self.current_viewing_day = int(packaged_data.get("view_day", 1))
                self.answer_visibility.clear()
                
                # Autofill inputs in the sidebar matching the loaded file
                self.subject_entry.delete(0, tk.END)
                self.subject_entry.insert(0, self.current_plan.get("subject", ""))
                self.topic_entry.delete(0, tk.END)
                self.topic_entry.insert(0, self.current_plan.get("topic", ""))
                
                days_count = len(self.current_plan["days"])
                self.days_slider.set(days_count)
                
                target_cls = self.current_plan.get("target_class", "JEE Main (PCM)")
                if target_cls in self.class_combobox['values']:
                    self.class_combobox.set(target_cls)
                    
                self.render_plan_dashboard()
                messagebox.showinfo("Load Successful", f"Revision plan successfully restored from:\n{os.path.basename(file_path)}")
            else:
                messagebox.showerror("Format Error", "The selected JSON file does not conform to the RevisionIO schema standard.")
        except Exception as e:
            messagebox.showerror("Read Error", f"Could not load revision roadmap file.\n\nDetails:\n{e}")


# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = RevisionIOApp(root)
    root.mainloop()
