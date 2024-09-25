import tkinter as tk
from tkinter import messagebox

class HousingPreferenceChatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("주거 선호도 조사 챗봇")
        self.master.geometry("400x500")

        self.questions = [
            ("가족 구성원 수를 알려주세요.", ["1인", "2인", "3인", "4인", "5인 이상"]),
            ("원하는 방의 갯수를 선택해주세요.", ["방 1개", "방 2개", "방 3개", "방 4개"]),
            ("원하는 화장실/욕실 갯수를 선택해주세요.", ["1개", "2개", "상관없음"]),
            ("집에서 가장 중요한 공간 요소 무엇인가요? (최대 2개 선택)", 
             ["키친 / 주방", "욕실 / 화장실", "식사 공간", "침실 / 휴식 공간", "거실", "업무 / 작업 공간", "아이방"]),
            ("아래 중 나의 드림 하우스에 꼭 반영되면 좋겠다고 생각하는 집의 요소는 무엇인가요? (복수 선택)",
             ["요리가 하고 싶어지는 넓은 주방", "가족이 다함께 모일 수 있는 넓은 리빙 다이닝", 
              "힐링할 수 있는 넓은 욕실", "고급 호텔처럼 화장실과 욕실이 분리된 건식 화장실", 
              "자녀와 분리된 생활 공간", "넓은 클로젯 (옷장)", "테라스 / 발코니", 
              "다용도실 또는 수납을 많이 할 수 있는 공간"])
        ]
        
        self.current_question = 0
        self.answers = []

        self.question_label = tk.Label(master, text="", wraplength=380)
        self.question_label.pack(pady=10)

        self.var = tk.StringVar()
        self.radio_buttons = []
        
        self.next_button = tk.Button(master, text="다음", command=self.next_question)
        self.next_button.pack(pady=10)

        self.show_question()

    def show_question(self):
        question, options = self.questions[self.current_question]
        self.question_label.config(text=question)

        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons.clear()

        if self.current_question in [3, 4]:  # 다중 선택 문항
            self.var = tk.StringVar()
            for option in options:
                cb = tk.Checkbutton(self.master, text=option, variable=tk.StringVar(), onvalue=option, offvalue="")
                cb.pack(anchor="w")
                self.radio_buttons.append(cb)
        else:  # 단일 선택 문항
            self.var = tk.StringVar()
            for option in options:
                rb = tk.Radiobutton(self.master, text=option, variable=self.var, value=option)
                rb.pack(anchor="w")
                self.radio_buttons.append(rb)

    def next_question(self):
        if self.current_question in [3, 4]:  # 다중 선택 문항
            selected = [cb.cget("variable").get() for cb in self.radio_buttons if cb.cget("variable").get()]
            if len(selected) == 0:
                messagebox.showwarning("경고", "최소 한 개 이상 선택해주세요.")
                return
            if self.current_question == 3 and len(selected) > 2:
                messagebox.showwarning("경고", "최대 2개까지만 선택 가능합니다.")
                return
            self.answers.append(selected)
        else:  # 단일 선택 문항
            if not self.var.get():
                messagebox.showwarning("경고", "옵션을 선택해주세요.")
                return
            self.answers.append(self.var.get())

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        result = "선택하신 답변:\n\n"
        for q, a in zip(self.questions, self.answers):
            result += f"{q[0]}\n답변: {', '.join(a) if isinstance(a, list) else a}\n\n"
        
        messagebox.showinfo("결과", result)
        self.master.quit()

root = tk.Tk()
chatbot = HousingPreferenceChatbot(root)
root.mainloop()
