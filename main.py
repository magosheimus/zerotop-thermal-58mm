"""
ZeroTop Thermal 58mm - Aplicativo para correção de margem superior em impressoras térmicas 58mm
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageOps
import os
import json
import ctypes
from image_processor import ImageProcessor
from printer_handler import PrinterHandler


def load_icon_image(icon_name, size=(32, 32)):
    """Carrega um ícone .ico e retorna como PhotoImage"""
    try:
        if os.path.exists(icon_name):
            img = Image.open(icon_name)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
    except:
        pass
    return None


def enable_dpi_awareness():
    """Habilita DPI awareness para evitar fonte borrada no Windows"""
    try:
        # Tenta configurar DPI awareness (Windows 8.1+)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            # Fallback para Windows Vista/7
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass


class TopStartThermalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroTop Thermal 58mm")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)  # Tamanho mínimo para acomodar 2 colunas
        self.root.configure(bg="#3165c4")  # Azul para combinar com a borda
        
        # Configurar estilos vintage Windows
        self.setup_styles()
        
        # Definir ícone da janela
        try:
            if os.path.exists("printer.ico"):
                self.root.iconbitmap("printer.ico")
        except:
            pass
        
        # Configurações
        self.PAPER_WIDTH_MM = 58
        self.DPI = 203
        self.PIXELS_PER_MM = 8
        self.PAPER_WIDTH_PX = 384  # Reduzido para compensar margens da impressora térmica
        
        # Estado
        self.original_image = None
        self.processed_image = None
        self.current_file = None
        self.auto_top_fix = tk.BooleanVar(value=True)
        self.manual_offset = tk.IntVar(value=0)
        self.num_copies = tk.IntVar(value=1)
        self.history_file = "history.json"
        self.image_history = self.load_history()
        self.thumbnail_buttons = []
        
        # Carregar ícones
        self.icon_printer_header = load_icon_image("printer.ico", (48, 48))
        self.icon_printer = load_icon_image("printer.ico", (32, 32))
        self.icon_printer_small = load_icon_image("printer.ico", (24, 24))
        self.icon_open_folder = None
        
        # Processadores
        self.image_processor = ImageProcessor(self.PAPER_WIDTH_PX, self.PIXELS_PER_MM)
        self.printer_handler = PrinterHandler()
        
        self.setup_ui()
        
        # Atalho: Enter para imprimir
        self.root.bind('<Return>', lambda event: self.print_image())
    
    def setup_styles(self):
        """Configura estilos personalizados para a interface - Tema Vintage Windows"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botões principais - Windows 95/98 Blue
        style.configure('Primary.TButton',
                       background='#316ac5',
                       foreground='#ffffff',
                       borderwidth=2,
                       focuscolor='#003c74',
                       padding=8,
                       relief='raised',
                       font=('MS Sans Serif', 9, 'bold'))
        style.map('Primary.TButton',
                 background=[('active', '#3e85f7'), ('pressed', '#003c74'), ('disabled', '#d3d0c7')],
                 foreground=[('disabled', '#868479')],
                 relief=[('pressed', 'sunken')])
        
        # Estilo para botão secundário - Windows Classic Gray
        style.configure('Secondary.TButton',
                       background='#ece9d8',
                       foreground='#000000',
                       borderwidth=2,
                       focuscolor='#aba798',
                       padding=8,
                       relief='raised',
                       font=('MS Sans Serif', 9))
        style.map('Secondary.TButton',
                 background=[('active', '#ffffff'), ('pressed', '#d3d0c7'), ('disabled', '#d3d0c7')],
                 foreground=[('disabled', '#868479')],
                 relief=[('pressed', 'sunken')])
        
        # Estilo para frames - Windows Classic Beige
        style.configure('Card.TFrame',
                       background='#f0eee4',
                       relief='flat')
        
        # Estilo para LabelFrame - Classic Windows com borda azul
        style.configure('TLabelframe',
                       background='#f0eee4',
                       borderwidth=3,
                       relief='ridge')
        style.configure('TLabelframe.Label',
                       background='#f0eee4',
                       foreground='#215dc6',
                       font=('MS Sans Serif', 9, 'bold'))
        
        # Estilo para Labels
        style.configure('TLabel',
                       background='#f0eee4',
                       foreground='#000000',
                       font=('MS Sans Serif', 8))
        
        # Estilo para Frames genéricos
        style.configure('TFrame',
                       background='#f0eee4')
        
        # Estilo para Spinbox
        style.configure('TSpinbox',
                       background='#ffffff',
                       foreground='#000000',
                       fieldbackground='#ffffff',
                       borderwidth=1,
                       font=('MS Sans Serif', 8))
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Header com ícone e título (tocar as bordas da janela)
        header_frame = tk.Frame(self.root, bg="#3165c4", relief='flat', borderwidth=0)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Frame para centralizar o conteúdo do header
        header_content = tk.Frame(header_frame, bg="#3165c4", pady=10)
        header_content.pack()
        
        # Ícone de impressora (usando .ico)
        icon_label = tk.Label(
            header_content,
            image=self.icon_printer_header if self.icon_printer_header else None,
            text="🖨️" if not self.icon_printer_header else "",
            font=("Segoe UI Emoji", 32),
            bg="#3165c4",
            fg="#ffffff"
        )
        icon_label.pack(side=tk.LEFT, padx=(10, 10))
        
        # Frame para título e subtítulo
        text_frame = tk.Frame(header_content, bg="#3165c4")
        text_frame.pack(side=tk.LEFT)
        
        # Título
        title_label = tk.Label(
            text_frame, 
            text="ZeroTop Thermal 58mm", 
            font=("MS Sans Serif", 18, "bold"),
            bg="#3165c4",
            fg="#ffffff"
        )
        title_label.pack(anchor=tk.W)
        
        # Subtítulo
        subtitle_label = tk.Label(
            text_frame, 
            text="Correção automática de margem superior para\nimpressoras térmicas 58mm", 
            font=("MS Sans Serif", 8),
            bg="#3165c4",
            fg="#ffffff",
            justify=tk.LEFT
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Frame principal com borda
        main_outer_frame = tk.Frame(self.root, bg="#3165c4", borderwidth=3, relief='raised')
        main_outer_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        main_frame = ttk.Frame(main_outer_frame, padding="12", style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Container de 2 colunas
        columns_frame = ttk.Frame(main_frame, style='Card.TFrame')
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid para proporção 1:2 (esquerda 1/3, direita 2/3)
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.columnconfigure(1, weight=2)
        columns_frame.rowconfigure(0, weight=1)
        
        # COLUNA ESQUERDA - Controles (1/3 da largura)
        left_column = ttk.Frame(columns_frame, style='Card.TFrame')
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Botão de abrir imagem
        open_btn = ttk.Button(
            left_column,
            text="📂 Abrir Imagem",
            command=self.open_image
        )
        open_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Histórico de imagens como miniaturas
        if self.image_history:
            history_frame = ttk.LabelFrame(left_column, text="Imagens Recentes", padding="5")
            history_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Frame com scroll para as miniaturas
            thumbnails_container = ttk.Frame(history_frame)
            thumbnails_container.pack(fill=tk.X)
            
            self.thumbnail_buttons = []
            for idx, img_path in enumerate(self.image_history[:5]):  # Mostrar até 5 recentes
                if os.path.exists(img_path):
                    try:
                        # Criar miniatura
                        img = Image.open(img_path)
                        img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        # Botão com miniatura
                        btn = tk.Button(
                            thumbnails_container,
                            image=photo,
                            command=lambda p=img_path: self.load_image_from_path(p),
                            relief='raised',
                            borderwidth=2,
                            bg='#ffffff',
                            cursor='hand2'
                        )
                        btn.image = photo  # Manter referência
                        btn.pack(side=tk.LEFT, padx=2, pady=2)
                        self.thumbnail_buttons.append(btn)
                    except:
                        pass
        
        # Controles adicionais
        controls_frame = ttk.LabelFrame(left_column, text="Controles", padding="10")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto Top Fix
        auto_fix_check = ttk.Checkbutton(
            controls_frame,
            text="Auto Top Fix (remover margem branca superior)",
            variable=self.auto_top_fix,
            command=self.update_preview
        )
        auto_fix_check.pack(anchor=tk.W, pady=5)
        
        # Offset manual
        offset_frame = ttk.Frame(controls_frame)
        offset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(offset_frame, text="Offset manual (mm):").pack(side=tk.LEFT, padx=(0, 10))
        offset_spinbox = ttk.Spinbox(
            offset_frame,
            from_=-50,
            to=50,
            textvariable=self.manual_offset,
            width=10,
            command=self.update_preview
        )
        offset_spinbox.pack(side=tk.LEFT)
        
        # Quantidade de cópias
        copies_frame = ttk.Frame(controls_frame)
        copies_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(copies_frame, text="Quantidade de cópias:").pack(side=tk.LEFT, padx=(0, 10))
        copies_spinbox = ttk.Spinbox(
            copies_frame,
            from_=1,
            to=100,
            textvariable=self.num_copies,
            width=10
        )
        copies_spinbox.pack(side=tk.LEFT)
        
        # Informações
        info_frame = ttk.LabelFrame(left_column, text="Informações:", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = tk.Label(
            info_frame,
            text="Nenhuma imagem carregada",
            font=("MS Sans Serif", 8),
            bg="#f0eee4",
            fg="#000000",
            justify=tk.LEFT,
            anchor=tk.W,
            wraplength=280
        )
        self.info_label.pack(fill=tk.X)
        
        # Botão de impressão (parte inferior da coluna esquerda)
        self.print_btn = ttk.Button(
            left_column,
            text="🖨️ IMPRIMIR",
            command=self.print_image,
            style='Primary.TButton'
        )
        self.print_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.print_btn.config(state='disabled')
        
        # COLUNA DIREITA - Preview (2/3 da largura)
        right_column = ttk.Frame(columns_frame, style='Card.TFrame')
        right_column.grid(row=0, column=1, sticky='nsew')
        
        # Preview área
        preview_frame = ttk.LabelFrame(right_column, text="Preview da Impressão", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame com borda pontilhada para o preview
        preview_border = tk.Frame(preview_frame, bg="#b0b0b0", relief='sunken', borderwidth=2)
        preview_border.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # Canvas para preview com estilo pontilhado
        self.preview_canvas = tk.Canvas(
            preview_border,
            bg="#ffffff",
            width=550,
            height=600,
            highlightthickness=0,
            relief='flat'
        )
        self.preview_canvas.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
        
        # Desenhar borda pontilhada no canvas
        self.preview_canvas.bind('<Configure>', self._draw_dotted_border)
        
        # Configurar drag and drop no canvas
        self.preview_canvas.drop_target_register(DND_FILES)
        self.preview_canvas.dnd_bind('<<Drop>>', self.on_drop)
        
        # Texto de ajuda para drag and drop
        self.placeholder_text_id = self.preview_canvas.create_text(
            275, 300,
            text=": Nenhuma imagem carregada",
            fill="#888888",
            font=("MS Sans Serif", 9),
            tags="placeholder"
        )
        
        # Barra de progresso decorativa na parte inferior do preview
        self.progress_bar_bg = self.preview_canvas.create_rectangle(
            20, 580, 530, 595,
            fill="#c0c0c0",
            outline="#808080",
            width=2,
            tags="progress_bg"
        )
        self.progress_bar = self.preview_canvas.create_rectangle(
            20, 580, 20, 595,
            fill="#52a8ff",
            outline="",
            tags="progress"
        )
    
    def _draw_dotted_border(self, event=None):
        """Desenha borda pontilhada no canvas de preview"""
        if not hasattr(self, 'preview_canvas'):
            return
        
        width = self.preview_canvas.winfo_width()
        height = self.preview_canvas.winfo_height()
        
        # Remover bordas antigas
        self.preview_canvas.delete("dotted_border")
        
        # Desenhar borda pontilhada
        margin = 10
        self.preview_canvas.create_rectangle(
            margin, margin, width - margin, height - margin,
            outline="#888888",
            width=2,
            dash=(5, 5),
            tags="dotted_border"
        )
    
    def load_history(self):
        """Carrega histórico de imagens do arquivo JSON"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_history(self):
        """Salva histórico de imagens no arquivo JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.image_history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add_to_history(self, file_path):
        """Adiciona arquivo ao histórico (máximo 10 itens)"""
        # Remover se já existe
        if file_path in self.image_history:
            self.image_history.remove(file_path)
        
        # Adicionar no início
        self.image_history.insert(0, file_path)
        
        # Limitar a 10 itens
        self.image_history = self.image_history[:10]
        
        # Salvar
        self.save_history()
        
        # Atualizar combobox se existir
        if hasattr(self, 'history_combo'):
            self.history_combo['values'] = self.image_history
    
    def load_image_from_path(self, path):
        """Carrega imagem a partir de um caminho"""
        if path and os.path.exists(path):
            self.load_image(path)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado!")
    
    def on_drop(self, event):
        """Handler para drag and drop"""
        # Obter o caminho do arquivo
        file_path = event.data
        
        # Remover chaves {} se existirem (Windows)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        # Remover espaços extras
        file_path = file_path.strip()
        
        # Carregar a imagem
        if os.path.isfile(file_path):
            self.load_image(file_path)
    
    def open_image(self):
        """Abre diálogo para selecionar imagem"""
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Carrega e processa a imagem"""
        try:
            # Carregar imagem original
            self.current_file = file_path
            self.original_image = Image.open(file_path)
            
            # Adicionar ao histórico
            self.add_to_history(file_path)
            
            # Processar imagem
            self.process_image()
            
            # Atualizar preview
            self.update_preview()
            
            # Habilitar botão de impressão
            self.print_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")
    
    def process_image(self):
        """Processa a imagem aplicando correções"""
        if not self.original_image:
            return
        
        # Redimensionar para largura correta (464px)
        self.processed_image = self.image_processor.resize_to_width(self.original_image)
        
        # Aplicar auto top fix se habilitado
        if self.auto_top_fix.get():
            self.processed_image = self.image_processor.remove_top_margin(self.processed_image)
        
        # Aplicar offset manual
        offset_mm = self.manual_offset.get()
        if offset_mm != 0:
            self.processed_image = self.image_processor.apply_offset(
                self.processed_image,
                offset_mm
            )
    
    def update_preview(self):
        """Atualiza o preview da imagem"""
        if not self.original_image:
            return
        
        # Reprocessar com configurações atuais
        self.process_image()
        
        # Limpar canvas
        self.preview_canvas.delete("all")
        
        # Remover placeholder se existir
        self.preview_canvas.delete("placeholder")
        
        # Obter dimensões do canvas
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        # Se o canvas ainda não foi renderizado, usar valores padrão
        if canvas_width <= 1:
            canvas_width = 550
            canvas_height = 600
        
        # Criar preview redimensionado para caber no canvas
        preview_image = self.processed_image.copy()
        preview_image.thumbnail((canvas_width - 40, canvas_height - 40), Image.Resampling.LANCZOS)
        
        # Converter para PhotoImage
        self.photo_preview = ImageTk.PhotoImage(preview_image)
        
        # Calcular posição centralizada
        center_x = canvas_width // 2
        start_y = 30
        
        # Desenhar no canvas (centralizado)
        self.preview_canvas.create_image(
            center_x, start_y,
            anchor=tk.N,
            image=self.photo_preview
        )
        
        # Desenhar indicador de topo (linha vermelha)
        margin = 20
        self.preview_canvas.create_line(
            margin, start_y, canvas_width - margin, start_y,
            fill="red",
            width=2,
            dash=(5, 5)
        )
        
        # Texto indicador de topo
        self.preview_canvas.create_text(
            center_x, start_y - 20,
            text="INÍCIO DA IMPRESSÃO (Y=0)",
            fill="red",
            font=("MS Sans Serif", 7, "bold"),
            anchor=tk.N
        )
        
        # Atualizar informações
        height_mm = self.processed_image.height / self.PIXELS_PER_MM
        self.info_label.config(
            text=f"Dimensões: {self.processed_image.width}x{self.processed_image.height}px\n"
                 f"Altura: {height_mm:.1f}mm | Largura: {self.PAPER_WIDTH_MM}mm"
        )
        
        # Atualizar barra de progresso decorativa (simular 100%)
        canvas_width = self.preview_canvas.winfo_width()
        if canvas_width > 1:
            self.preview_canvas.coords(self.progress_bar, 20, 580, canvas_width - 20, 595)
    
    def print_image(self):
        """Envia imagem para impressão"""
        if not self.processed_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        
        try:
            # Converter para monocromático para impressão térmica
            print_image = self.image_processor.convert_to_monochrome(self.processed_image)
            
            # Obter quantidade de cópias
            num_copies = self.num_copies.get()
            
            # Imprimir múltiplas cópias
            success_count = 0
            for i in range(num_copies):
                success = self.printer_handler.print_image(print_image)
                if success:
                    success_count += 1
            
            if success_count == num_copies:
                messagebox.showinfo("Sucesso", f"{num_copies} cópia(s) enviada(s) com sucesso!")
            elif success_count > 0:
                messagebox.showwarning("Parcial", f"{success_count} de {num_copies} cópia(s) impressa(s)")
            else:
                messagebox.showerror("Erro", "Falha ao enviar para impressora")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir: {str(e)}")
    


def main():
    # Habilitar DPI awareness ANTES de criar a janela Tkinter
    enable_dpi_awareness()
    
    root = TkinterDnD.Tk()
    app = TopStartThermalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
