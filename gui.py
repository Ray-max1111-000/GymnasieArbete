import os
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from main import PasswordManagerCore
import string

class JokerEncryptionGUI:
    def __init__(self, root):
        self.core = PasswordManagerCore()
        self.root = root
        self.root.withdraw()
        self.chaos_mode = False
        self.setup_styles()
        self.create_splash_screen()
        self.root.after(20000, self.initialize_app)
        self.current_quote = 0
        self.smoke_particles = []

    def create_splash_screen(self):
        """Create splash screen with animated status messages"""
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.splash.configure(background=self.colors['background'])
        
        # Center splash screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_size = 400
        x = (screen_width - splash_size) // 2
        y = (screen_height - splash_size) // 2
        self.splash.geometry(f"{splash_size}x{splash_size}+{x}+{y}")

        try:
            self.root.iconbitmap('joker.ico')
        except:
            pass

        try:
            # Ladda och visa logon
            self.logo_image = tk.PhotoImage(file='joker.png').subsample(2, 2)
            self.logo_label = ttk.Label(self.splash, image=self.logo_image, 
                                      background=self.colors['background'])
            self.logo_label.pack(pady=15)

            # Animerad status för text
            self.status_text = ttk.Label(
                self.splash,
                text="Initializing Chaos Cipher...",
                foreground=self.colors['accent'],
                background=self.colors['background'],
                font=('Algerian', 12, 'bold')
            )
            self.status_text.pack(pady=10)

            # Joker-tema progress bar
            self.splash_progress = ttk.Progressbar(
                self.splash,
                orient='horizontal',
                mode='determinate',
                length=300,
                maximum=100,
                style='Joker.Horizontal.TProgressbar'
            )
            self.splash_progress.pack(pady=15)

            # Starta animationen
            self.update_loading_message()
            self.update_progress()

        except Exception as e:
            messagebox.showwarning("Logo Error", f"Could not load logo image: {str(e)}")
            self.splash.destroy()

    def animate_smoke(self):
        """Create green and purple smoke animation effect"""
        if self.chaos_mode:
            self.smoke_canvas = tk.Canvas(self.root, bg=self.colors['background'], 
                                        highlightthickness=0)
            self.smoke_canvas.place(relwidth=1, relheight=1)

            def create_particle():
                x = random.randint(0, self.root.winfo_width())
                y = self.root.winfo_height()
                colors = ['#39ff14', '#7a00cc']
                particle = self.smoke_canvas.create_oval(
                    x, y, x+30, y+30,
                    fill=random.choice(colors),
                    width=0,
                    alpha=.3
                )
                self.smoke_particles.append(particle)

            def move_particles():
                for particle in self.smoke_particles:
                    self.smoke_canvas.move(
                        particle,
                        random.randint(-2, 2),
                        random.randint(-10, -5)
                    )
                    self.smoke_canvas.itemconfig(
                        particle,
                        alpha=max(0, float(self.smoke_canvas.itemcget(particle, "alpha")) - 0.01)
                    )
                self.root.after(50, move_particles)

            self.root.after(100, create_particle)
            self.root.after(100, move_particles)

    def update_loading_message(self):
        """Cycle through security status messages"""
        messages = [
            "Injecting Chaos Serum...",
            "Corrupting Gotham Databases...",
            "Activating Laughing Gas Protocol...",
            "Encrypting with Ha-Ha-Hybrid Algorithm...",
            "Initializing Smilex Encryption...",
            "Synchronizing Chaos Theory Patterns..."
        ]
        new_msg = random.choice(messages)
        self.status_text.config(text=new_msg)
        self.splash.after(3000, self.update_loading_message)

    def update_progress(self):
        """Animate progress bar"""
        current = self.splash_progress['value']
        if current < 100:
            increment = random.uniform(0.5, 2.5)
            self.splash_progress['value'] = min(current + increment, 100)
            self.splash.after(100, self.update_progress)

    def initialize_app(self):
        """Cleanup splash and start main app"""
        try:
            self.splash.destroy()
            self.root.after_cancel(self.update_loading_message)
            self.root.after_cancel(self.update_progress)
        except:
            pass
        
        self.root.deiconify()
        self.setup_ui()
        self.check_initialization()
        self.root.config(cursor="spider")
        self.animate_smoke()
        self.cycle_joker_quotes()

    def cycle_joker_quotes(self):
        """Show random Joker quotes in status bar"""
        quotes = [
            "Why so serious?",
            "Let's put a smile on that face!",
            "I believe whatever doesn't kill you makes you... stranger",
            "Introduce a little anarchy!",
            "This town deserves a better class of security...",
            "Madness is like gravity - all it needs is a little push!"
        ]
        if not self.status_bar['text'].startswith("✓"):
            self.status_bar.config(text=random.choice(quotes))
        self.root.after(10000, self.cycle_joker_quotes)

    def rot13_filename(self):
        """ROT13 encrypted filename"""
        return 'cnffjbeqf.wfqv'

    def setup_styles(self):
        """Apply Joker-inspired color scheme"""
        self.style = ttk.Style()
        self.colors = {
            'background': '#0d0d0d',
            'foreground': '#ffffff',
            'accent': '#7a00cc',
            'secondary': '#2a1a33',
            'text': '#c7a2d1',
            'success': '#39ff14',
            'error': '#ff003c'
        }

        self.style.theme_use('clam')
        
        # Custom progress bar style
        self.style.element_create('Joker.Progressbar.trough', 'from', 'clam')
        self.style.element_create('Joker.Progressbar.pbar', 'from', 'clam')
        self.style.layout('Joker.Horizontal.TProgressbar',
            [('Joker.Progressbar.trough', {
                'sticky': 'nswe',
                'children': [('Joker.Progressbar.pbar', {
                    'side': 'left',
                    'sticky': 'ns'
                })]
            })]
        )
        self.style.configure('Joker.Horizontal.TProgressbar',
            background=self.colors['accent'],
            troughcolor=self.colors['secondary'],
            bordercolor=self.colors['accent'],
            lightcolor=self.colors['success'],
            darkcolor=self.colors['accent']
        )

        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], 
                           foreground=self.colors['foreground'], font=('Verdana', 10))
        self.style.configure('TButton', background=self.colors['accent'], 
                           foreground=self.colors['foreground'], font=('Verdana', 10, 'bold'), 
                           padding=6, borderwidth=0)
        self.style.map('TButton', 
                      background=[('active', '#5a0099')], 
                      foreground=[('active', '#ffffff')])
        self.style.configure('TEntry', fieldbackground=self.colors['secondary'], 
                           foreground=self.colors['foreground'], 
                           insertcolor=self.colors['foreground'], padding=4)
        self.style.configure('TLabelframe', background=self.colors['background'], 
                           foreground=self.colors['accent'])
        self.style.configure('Treeview', background=self.colors['secondary'], 
                           fieldbackground=self.colors['secondary'], 
                           foreground=self.colors['foreground'])
    def toggle_chaos_mode(self):
        """Activate random color chaos"""
        self.chaos_mode = not self.chaos_mode
        if self.chaos_mode:
            self.animate_chaos_colors()

    def animate_chaos_colors(self):
        """Randomly change accent colors"""
        if self.chaos_mode:
            colors = ['#7a00cc', '#39ff14', '#ff003c', '#ff9500', '#00ffff']
            new_color = random.choice(colors)
            
            # Updatera UI elements
            self.style.configure('TButton', background=new_color)
            self.style.configure('TLabelframe', foreground=new_color)
            self.status_bar.config(foreground=new_color)
            
            # Recall efter 2 seconds
            self.root.after(2000, self.animate_chaos_colors)

    def check_initialization(self):
        """Check if encryption system is initialized"""
        if not os.path.exists("chaos_cipher.key"):
            self.show_first_run_wizard()
        else:
            self.authenticate_user()

    def show_first_run_wizard(self):
        """Initial setup wizard"""
        pw = simpledialog.askstring("First Run Setup", 
                                  "Create a master password (min 12 characters):\nWhy so serious?", 
                                  show='*')
        if not pw or len(pw) < 12:
            messagebox.showerror("Error", "Let's put a smile on that password! Too short!")
            self.root.destroy()
            return
        try:
            self.core.initialize_encryption(pw)
            messagebox.showinfo("Success", "System initialized!\nNow let's make some magic!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")
            self.root.destroy()

    def authenticate_user(self):
        """Password authentication dialog"""
        while True:
            pw = simpledialog.askstring("Authentication", 
                                      "Enter master password:\nLet's see your best trick!", 
                                      show='*')
            if not pw:
                self.root.destroy()
                return
            try:
                self.core.load_encryption(pw)
                break
            except Exception as e:
                messagebox.showerror("Error", f"Wrong move! {str(e)}")

    def setup_ui(self):
        """Initialize main application UI"""
        self.root.title("Joker Encryption v1.0")
        self.root.geometry("900x700")
        self.root.minsize(400, 600)
        self.root.configure(bg=self.colors['background'])

        # Chaos Mode menu
        menubar = tk.Menu(self.root)
        chaos_menu = tk.Menu(menubar, tearoff=0)
        chaos_menu.add_command(label="Toggle Chaos Mode", command=self.toggle_chaos_mode)
        menubar.add_cascade(label="Madness", menu=chaos_menu)
        self.root.config(menu=menubar)

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="🎭 Joker Encryption v1.0", 
                font=('Impact', 20), 
                foreground=self.colors['accent']).pack(side=tk.LEFT)

        # Main content
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Entry form
        left_frame = ttk.LabelFrame(content_frame, text="New Chaos Entry")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        entry_fields = [
            ("🌐 Shadow Network", "entry_website"),
            ("👤 Alter Ego", "entry_username"),
            ("🔑 Secret Laugh", "entry_password")
        ]

        for label, field in entry_fields:
            frame = ttk.Frame(left_frame)
            frame.pack(fill=tk.X, pady=8)
            
            ttk.Label(frame, text=label, width=15).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame)
            entry.pack(fill=tk.X, expand=True, padx=5)
            setattr(self, field, entry)

        self.entry_password.config(show="•")

        # Action buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=15)

        ttk.Button(btn_frame, text="Generate Chaos Code", 
                 command=self.generate_password).pack(side=tk.LEFT, expand=True)
        ttk.Button(btn_frame, text="Lock It In", 
                 command=self.save_entry).pack(side=tk.RIGHT, expand=True)

        # Right panel - Password list
        right_frame = ttk.LabelFrame(content_frame, text="Stored Secrets")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Treeview with scrollbar
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("website", "username"), 
                               show="headings", selectmode="browse")
        
        self.tree.heading("website", text="Shadow Network", anchor=tk.W)
        self.tree.heading("username", text="Alter Ego", anchor=tk.W)
        self.tree.column("website", width=200)
        self.tree.column("username", width=150)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Reveal Secret", command=self.copy_selected_password)
        self.context_menu.add_command(label="Burn Evidence", command=self.delete_selected_entry)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.show_password_details)

        # Status bar
        self.status_bar = ttk.Label(self.root, 
                                  text="🔐 Secrets encrypted with chaotic entropy",
                                  relief=tk.SUNKEN,
                                  anchor=tk.W,
                                  font=('Verdana', 8),
                                  foreground=self.colors['text'],
                                  background=self.colors['secondary'])
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.refresh_list()

    def refresh_list(self):
        """Refresh secret list"""
        self.tree.delete(*self.tree.get_children())
        try:
            for entry in self.core.load_passwords():
                self.tree.insert("", tk.END, values=(entry["website"], entry["username"]))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load secrets: {str(e)}")

    def save_entry(self):
        """Save new secret entry"""
        entry = {
            "website": self.entry_website.get(),
            "username": self.entry_username.get(),
            "password": self.entry_password.get()
        }

        if not all(entry.values()):
            messagebox.showwarning("Error", "All fields must be filled!\nThe devil's in the details...")
            return

        try:
            self.core.save_password_entry(entry)
            self.refresh_list()
            self.entry_website.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            messagebox.showinfo("Success", "Secret locked away!\nIt'll be our little joke...")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {str(e)}")

    def generate_password(self):
        """Generate chaotic password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*_+=~"
        password = ''.join(random.choice(chars) for _ in range(24))
        self.entry_password.delete(0, tk.END)
        self.entry_password.insert(0, password)
        self.copy_to_clipboard(password)

    def show_password_details(self, event):
        """Show secret details on double-click"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        website = item["values"][0]
        
        try:
            entries = self.core.load_passwords()
            entry = next(e for e in entries if e["website"] == website)
            
            detail_window = tk.Toplevel(self.root)
            detail_window.title("Secret Details")
            detail_window.geometry("400x250")
            detail_window.configure(bg=self.colors['background'])
            
            fields = [
                ("Shadow Network:", entry['website']),
                ("Alter Ego:", entry['username']),
                ("Secret Laugh:", entry['password'])
            ]
            
            for label, value in fields:
                frame = ttk.Frame(detail_window)
                frame.pack(fill=tk.X, pady=8, padx=20)
                
                ttk.Label(frame, text=label, width=15, 
                        font=('Verdana', 10, 'bold')).pack(side=tk.LEFT)
                ttk.Label(frame, text=value, 
                        font=('Verdana', 10)).pack(side=tk.LEFT)
                
            # Copy buttons
            btn_frame = ttk.Frame(detail_window)
            btn_frame.pack(pady=15)
            
            ttk.Button(btn_frame, text="Share Secret", 
                     command=lambda: self.copy_to_clipboard(entry['password']))\
                     .pack(side=tk.LEFT, padx=5)
            
            ttk.Button(btn_frame, text="Vanish", 
                     command=detail_window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal secret: {str(e)}")

    def copy_selected_password(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            website = item["values"][0]
            try:
                entries = self.core.load_passwords()
                entry = next(e for e in entries if e["website"] == website)
                self.copy_to_clipboard(entry['password'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy secret: {str(e)}")

    def delete_selected_entry(self):
        selection = self.tree.selection()
        if selection and messagebox.askyesno("Confirm Destruction", 
                                           "Burn this secret to ashes?\nThere's no going back..."):
            website = self.tree.item(selection[0])["values"][0]
            try:
                entries = self.core.load_passwords()
                entries = [e for e in entries if e["website"] != website]
                
                with open(self.rot13_filename(), "w") as f:
                    json.dump(entries, f, indent=4)
                
                self.refresh_list()
                messagebox.showinfo("Poof!", "Secret vanished without a trace!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to destroy secret: {str(e)}")

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_bar.config(text="✂️ Secret copied to clipboard - use wisely...")
        self.root.after(3000, lambda: self.status_bar.config(
            text="🔐 Secrets encrypted with chaotic entropy"))

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = JokerEncryptionGUI(root)
    root.mainloop()
        