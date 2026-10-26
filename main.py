import webbrowser
import threading
import requests
import customtkinter as ctk
Lazy import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RepositoryAnalyzer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitHub Repository Analyzer")
        self.geometry("980x720")
        self.minsize(850, 600)
        self.configure(fg_color="#18191c")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_control_panel()
        self._build_results_area()
        self._build_status_bar()

    def _build_header(self):
        header_frame = ctk.CTkFrame(
            self,
            fg_color="#212328",
            corner_radius=12,
            border_width=2,
            border_color="#32363e"
        )
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="GitHub Repository Analyzer",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#e6edf3"
        )
        title_label.grid(row=0, column=0, padx=24, pady=16, sticky="w")

        info_btn = ctk.CTkButton(
            header_frame,
            text="ℹ",
            width=38,
            height=38,
            corner_radius=10,
            fg_color="#2b2f38",
            hover_color="#383d49",
            border_width=2,
            border_color="#454b59",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.open_info_window
        )
        info_btn.grid(row=0, column=1, padx=20, pady=16, sticky="e")

    def _build_control_panel(self):
        panel = ctk.CTkFrame(
            self,
            fg_color="#1e2025",
            corner_radius=12,
            border_width=2,
            border_color="#2d313a"
        )
        panel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        lang_label = ctk.CTkLabel(panel, text="Language:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8b949e")
        lang_label.grid(row=0, column=0, padx=(18, 6), pady=16)

        self.lang_input = ctk.CTkEntry(
            panel,
            width=140,
            height=38,
            corner_radius=8,
            fg_color="#131417",
            border_color="#363b45",
            border_width=2,
            text_color="#f0f6fc"
        )
        self.lang_input.insert(0, "python")
        self.lang_input.grid(row=0, column=1, padx=6, pady=16)

        sort_label = ctk.CTkLabel(panel, text="Sort By:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8b949e")
        sort_label.grid(row=0, column=2, padx=(14, 6), pady=16)

        self.sort_option = ctk.CTkComboBox(
            panel,
            values=["stars", "forks", "updated"],
            width=130,
            height=38,
            corner_radius=8,
            fg_color="#131417",
            button_color="#2c3038",
            button_hover_color="#3d434f",
            border_color="#363b45",
            border_width=2,
            dropdown_fg_color="#1e2025"
        )
        self.sort_option.set("stars")
        self.sort_option.grid(row=0, column=3, padx=6, pady=16)

        limit_label = ctk.CTkLabel(panel, text="Count:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#8b949e")
        limit_label.grid(row=0, column=4, padx=(14, 6), pady=16)

        self.limit_option = ctk.CTkComboBox(
            panel,
            values=["10", "20", "30", "50"],
            width=85,
            height=38,
            corner_radius=8,
            fg_color="#131417",
            button_color="#2c3038",
            button_hover_color="#3d434f",
            border_color="#363b45",
            border_width=2,
            dropdown_fg_color="#1e2025"
        )
        self.limit_option.set("15")
        self.limit_option.grid(row=0, column=5, padx=6, pady=16)

        self.fetch_btn = ctk.CTkButton(
            panel,
            text="Fetch Repositories",
            height=38,
            corner_radius=8,
            fg_color="#238636",
            hover_color="#2ea043",
            border_width=2,
            border_color="#3fb950",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.start_fetch_thread
        )
        self.fetch_btn.grid(row=0, column=6, padx=(20, 18), pady=16)

    def _build_results_area(self):
        container = ctk.CTkFrame(
            self,
            fg_color="#191b1f",
            corner_radius=12,
            border_width=2,
            border_color="#2c2f37"
        )
        container.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="#131417",
            corner_radius=8
        )
        self.scroll_frame.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self._render_placeholder()

    def _render_placeholder(self):
        self.empty_msg = ctk.CTkLabel(
            self.scroll_frame,
            text="Select filters and click 'Fetch Repositories' to load data.",
            font=ctk.CTkFont(size=14),
            text_color="#6e7681"
        )
        self.empty_msg.pack(pady=120)

    def _build_status_bar(self):
        self.status_bar = ctk.CTkLabel(
            self,
            text="Status: Ready",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color="#7d8590"
        )
        self.status_bar.grid(row=3, column=0, padx=26, pady=(0, 12), sticky="w")

    def start_fetch_thread(self):
        self.fetch_btn.configure(state="disabled", text="Fetching...")
        self.status_bar.configure(text="Status: Querying GitHub API...")
        thread = threading.Thread(target=self.fetch_data, daemon=True)
        thread.start()

    def fetch_data(self):
        language = self.lang_input.get().strip() or "python"
        sort_by = self.sort_option.get()
        per_page = int(self.limit_option.get())

        url = f"https://api.github.com/search/repositories?q=language:{language}&sort={sort_by}&order=desc&per_page={per_page}"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                payload = response.json()
                items = payload.get("items", [])
                self.after(0, self.display_cards, items)
            elif response.status_code == 403:
                msg = "Rate limit hit. GitHub limits unauthenticated requests to 60/hr. Try again later."
                self.after(0, self.display_error, msg)
            else:
                msg = f"HTTP Error {response.status_code}: Unable to pull repository records."
                self.after(0, self.display_error, msg)

        except requests.exceptions.Timeout:
            self.after(0, self.display_error, "Request timed out while connecting to GitHub.")
        except requests.exceptions.RequestException as err:
            self.after(0, self.display_error, f"Connection failed: {str(err)}")

    def display_cards(self, items):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not items:
            lbl = ctk.CTkLabel(self.scroll_frame, text="No matching repositories found.", text_color="#8b949e")
            lbl.pack(pady=80)
            self.status_bar.configure(text="Status: 0 repositories returned.")
            self.fetch_btn.configure(state="normal", text="Fetch Repositories")
            return

        for index, repo in enumerate(items, start=1):
            name = repo.get("full_name", "Unknown Repository")
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            desc = repo.get("description") or "No description provided."
            html_url = repo.get("html_url", "")

            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#1c1f24",
                corner_radius=10,
                border_width=2,
                border_color="#2e333d"
            )
            card.pack(fill="x", padx=10, pady=6)
            card.grid_columnconfigure(0, weight=1)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 4))
            top_row.grid_columnconfigure(0, weight=1)

            rank_and_name = ctk.CTkLabel(
                top_row,
                text=f"#{index}  {name}",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#58a6ff",
                anchor="w"
            )
            rank_and_name.grid(row=0, column=0, sticky="w")

            metrics = ctk.CTkLabel(
                top_row,
                text=f"★ {stars:,}   |   ⑂ {forks:,}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#d29922",
                anchor="e"
            )
            metrics.grid(row=0, column=1, sticky="e")

            desc_box = ctk.CTkLabel(
                card,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color="#adbac7",
                anchor="w",
                justify="left",
                wraplength=760
            )
            desc_box.grid(row=1, column=0, padx=16, pady=(4, 12), sticky="w")

            visit_btn = ctk.CTkButton(
                card,
                text="Open Repo ↗",
                width=100,
                height=28,
                corner_radius=6,
                fg_color="#262930",
                hover_color="#363b45",
                border_width=1,
                border_color="#454b59",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda url=html_url: webbrowser.open(url)
            )
            visit_btn.grid(row=1, column=1, padx=16, pady=(4, 12), sticky="e")

        self.status_bar.configure(text=f"Status: Displaying top {len(items)} repositories.")
        self.fetch_btn.configure(state="normal", text="Fetch Repositories")

    def display_error(self, message):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        err_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"Error: {message}",
            font=ctk.CTkFont(size=13),
            text_color="#f85149",
            wraplength=600
        )
        err_label.pack(pady=80)
        self.status_bar.configure(text="Status: Operation failed.")
        self.fetch_btn.configure(state="normal", text="Fetch Repositories")

    def open_info_window(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("About & Documentation")
        dialog.geometry("520x460")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#181a1f")
        dialog.transient(self)
        dialog.grab_set()

        outer_card = ctk.CTkFrame(
            dialog,
            fg_color="#20232a",
            corner_radius=12,
            border_width=2,
            border_color="#353b47"
        )
        outer_card.pack(fill="both", expand=True, padx=18, pady=18)

        meta_frame = ctk.CTkFrame(outer_card, fg_color="#17191e", corner_radius=8, border_width=1, border_color="#2b303c")
        meta_frame.pack(fill="x", padx=16, pady=(16, 12))

        dev_title = ctk.CTkLabel(meta_frame, text="Developer Profile", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e6edf3")
        dev_title.pack(anchor="w", padx=14, pady=(10, 4))

        dev_name = ctk.CTkLabel(meta_frame, text="Name: Atharva", font=ctk.CTkFont(size=13), text_color="#c9d1d9")
        dev_name.pack(anchor="w", padx=14, pady=2)

        links_frame = ctk.CTkFrame(meta_frame, fg_color="transparent")
        links_frame.pack(fill="x", padx=14, pady=(6, 12))

        gh_btn = ctk.CTkButton(
            links_frame,
            text="GitHub Profile",
            width=120,
            height=30,
            corner_radius=6,
            fg_color="#292e38",
            hover_color="#3a414f",
            border_width=1,
            border_color="#4f5768",
            command=lambda: webbrowser.open("https://github.com/")
        )
        gh_btn.pack(side="left", padx=(0, 10))

        li_btn = ctk.CTkButton(
            links_frame,
            text="LinkedIn Profile",
            width=120,
            height=30,
            corner_radius=6,
            fg_color="#0a66c2",
            hover_color="#084e96",
            border_width=1,
            border_color="#388bfd",
            command=lambda: webbrowser.open("https://linkedin.com/")
        )
        li_btn.pack(side="left")

        guide_frame = ctk.CTkFrame(outer_card, fg_color="#17191e", corner_radius=8, border_width=1, border_color="#2b303c")
        guide_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        guide_title = ctk.CTkLabel(guide_frame, text="How to Use This App", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e6edf3")
        guide_title.pack(anchor="w", padx=14, pady=(10, 4))

        instructions = (
            "1. Enter a programming language target (e.g., python, javascript, rust).\n"
            "2. Select a sorting parameter: stars, forks, or recently updated.\n"
            "3. Choose the number of repositories to query.\n"
            "4. Hit 'Fetch Repositories' to trigger the query.\n"
            "5. Click 'Open Repo ↗' on any card to launch it directly in your browser."
        )

        steps_label = ctk.CTkLabel(
            guide_frame,
            text=instructions,
            justify="left",
            font=ctk.CTkFont(size=12),
            text_color="#8b949e"
        )
        steps_label.pack(anchor="w", padx=14, pady=(4, 12))


if __name__ == "__main__":
    app = RepositoryAnalyzer()
    app.mainloop()
