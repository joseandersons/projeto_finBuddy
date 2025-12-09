import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json
import urllib.request
import urllib.error
from datetime import datetime

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

class FinancialChatBot:
    def __init__(self):
        self.history = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente financeiro básico chamado FinBuddy. "
                    "Explique conceitos simples de finanças pessoais, como orçamento, economia, juros simples e compostos, "
                    "planejamento financeiro, organização de gastos e criação de metas. "
                    "Use linguagem acessível, exemplos práticos e tom amigável. "
                    "Não dê recomendações de investimentos específicos, não indique ações, títulos ou criptomoedas. "
                    "Não oriente sobre sonegação de impostos ou nada ilegal. "
                    "Se a pergunta envolver algo muito complexo ou pessoal, recomende procurar um profissional de finanças ou contador."
                )
            }
        ]

    def send_message(self, user_message: str) -> str:
        try:
            self.history.append({"role": "user", "content": user_message})

            data = {
                "model": MODEL,
                "messages": self.history,
                "max_tokens": 500,
                "temperature": 0.7
            }

            json_data = json.dumps(data).encode("utf-8")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "FinBuddy ChatBot"
            }

            req = urllib.request.Request(
                API_URL,
                data=json_data,
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode("utf-8"))

            if "choices" in response_data and response_data["choices"]:
                bot_response = response_data["choices"][0]["message"]["content"]
                self.history.append({"role": "assistant", "content": bot_response})

                if len(self.history) > 12:
                    self.history = [self.history[0]] + self.history[-10:]

                return bot_response

            return "Erro: resposta vazia do modelo."

        except urllib.error.HTTPError as e:
            error_msg = f"Erro HTTP {e.code}"
            try:
                error_data = json.loads(e.read().decode("utf-8"))
                if "error" in error_data:
                    error_msg += f": {error_data['error'].get('message', 'Erro desconhecido')}"
            except Exception:
                pass
            return error_msg

        except Exception as e:
            return f"Erro de conexão: {str(e)[:120]}"

    def clear_history(self):
        self.history = [self.history[0]]

    def save_conversation(self, filename: str) -> bool:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("CONVERSA FINBUDDY\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("=" * 60 + "\n\n")

                for msg in self.history[1:]:
                    if msg["role"] == "user":
                        f.write(f"VOCÊ: {msg['content']}\n\n")
                    elif msg["role"] == "assistant":
                        f.write(f"FINBUDDY: {msg['content']}\n\n")

            return True
        except Exception:
            return False


class FinBuddyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FinBuddy - Assistente Financeiro Básico")
        self.root.geometry("750x600")

        self.chatbot = FinancialChatBot()

        self.setup_ui()
        print("FinBuddy inicializado.")

    def setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="FinBuddy - Assistente Financeiro Básico",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=20
        )
        self.chat_area.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.add_message("system", "Sistema", "FinBuddy pronto para responder suas perguntas sobre finanças pessoais.")

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12)
        )
        self.input_field.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            input_frame,
            text="Enviar",
            command=self.send_message,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white"
        )
        send_btn.pack(side=tk.RIGHT)

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        clear_btn = tk.Button(
            button_frame,
            text="Limpar",
            command=self.clear_chat,
            bg="#FF9800",
            fg="white"
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        save_btn = tk.Button(
            button_frame,
            text="Salvar conversa",
            command=self.save_chat,
            bg="#2196F3",
            fg="white"
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        exit_btn = tk.Button(
            button_frame,
            text="Sair",
            command=self.root.quit,
            bg="#F44336",
            fg="white"
        )
        exit_btn.pack(side=tk.RIGHT)

    def add_message(self, sender_type: str, sender: str, message: str):
        self.chat_area.config(state=tk.NORMAL)
        hora = datetime.now().strftime("%H:%M")

        self.chat_area.insert(tk.END, f"[{hora}] {sender}: {message}\n\n")

        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def send_message(self):
        message = self.input_field.get().strip()
        if not message:
            return

        self.add_message("user", "Você", message)
        self.input_field.delete(0, tk.END)

        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "FinBuddy está digitando...\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self.root.update()

        response = self.chatbot.send_message(message)

        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("end-2l", "end-1l")
        self.chat_area.config(state=tk.DISABLED)

        self.add_message("bot", "FinBuddy", response)

    def clear_chat(self):
        if messagebox.askyesno("Limpar", "Deseja limpar a conversa?"):
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete(1.0, tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.chatbot.clear_history()
            self.add_message("system", "Sistema", "Conversa limpa. Você pode começar novamente.")

    def save_chat(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            initialfile=f"conversa_finbuddy_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        )

        if filename:
            if self.chatbot.save_conversation(filename):
                messagebox.showinfo("Sucesso", "Conversa salva com sucesso.")
            else:
                messagebox.showerror("Erro", "Não foi possível salvar a conversa.")

    def run(self):
        self.root.mainloop()


def main():
    print("=" * 60)
    print("FINBUDDY - ASSISTENTE FINANCEIRO BÁSICO")
    print("=" * 60)
    print(f"Modelo: {MODEL}")
    print("=" * 60)

    try:
        urllib.request.urlopen("https://openrouter.ai", timeout=5)
        print("Conexão com OpenRouter: OK")
    except Exception:
        print("Sem conexão com a internet.")

    app = FinBuddyGUI()
    app.run()


if __name__ == "__main__":
    main()
