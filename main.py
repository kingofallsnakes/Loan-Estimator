from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder

# Kivy Language String
kv = """
<LoanCalculator>:
    orientation: 'vertical'
    padding: 20
    spacing: 20
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Loan Estimator"
        font_size: 36
        color: 1, 1, 1, 1
    Label:
        text: "Enter the loan amount: Rs:"
        font_size: 18
        color: 0.9, 0.9, 0.9, 1
    TextInput:
        id: principal_input
        input_filter: 'float'
        multiline: False
        background_color: 0.2, 0.2, 0.2, 1
        foreground_color: 1, 1, 1, 1
    Label:
        text: "Enter the annual interest rate (%): "
        font_size: 18
        color: 0.9, 0.9, 0.9, 1
    TextInput:
        id: interest_input
        input_filter: 'float'
        multiline: False
        background_color: 0.2, 0.2, 0.2, 1
        foreground_color: 1, 1, 1, 1
    Label:
        text: "Enter the loan term (in months): "
        font_size: 18
        color: 0.9, 0.9, 0.9, 1
    TextInput:
        id: months_input
        input_filter: 'int'
        multiline: False
        background_color: 0.2, 0.2, 0.2, 1
        foreground_color: 1, 1, 1, 1
    Button:
        text: "Estimation"
        on_press: root.calculate()
        background_color: 0.2, 0.6, 0.86, 1
        color: 1, 1, 1, 1
        font_size: 18
        size_hint_y: None
        height: 50
    Label:
        id: result_label
        text: ""
        font_size: 22
        color: 0.1, 0.8, 0.1, 1
    Label:
        id: monthly_payment_label
        text: ""
        font_size: 18
        color: 1, 1, 1, 1
    Label:
        id: daily_payment_label
        text: ""
        font_size: 18
        color: 1, 1, 1, 1
"""

# Load the kv string
Builder.load_string(kv)

class LoanCalculator(BoxLayout):

    def calculate_loan_payment(self, principal, annual_interest_rate, months):
        # Convert annual interest rate to monthly rate
        monthly_interest_rate = annual_interest_rate / 12 / 100

        # Calculate monthly payment
        if monthly_interest_rate == 0:
            monthly_payment = principal / months
        else:
            monthly_payment = (
                principal
                * (monthly_interest_rate * (1 + monthly_interest_rate) ** months)
                / ((1 + monthly_interest_rate) ** months - 1)
            )

        return monthly_payment

    def calculate(self):
        try:
            principal = float(self.ids.principal_input.text)
            annual_interest_rate = float(self.ids.interest_input.text)
            months = int(self.ids.months_input.text)

            monthly_payment = self.calculate_loan_payment(principal, annual_interest_rate, months)
            self.daily_payment = monthly_payment / 30  # Assuming 30 days in a month

            self.ids.result_label.text = f"Your monthly payment will be: ${monthly_payment:.2f}"

            # Update the monthly and daily payment labels
            self.ids.monthly_payment_label.text = f"Monthly Payment: Rs {monthly_payment:.2f}"
            self.ids.daily_payment_label.text = f"Daily Payment: Rs {self.daily_payment:.2f}"

        except ValueError:
            self.show_error("Please enter valid numbers")

    def show_error(self, message):
        popup = Popup(title='Input Error', content=Label(text=message), size_hint=(None, None), size=(600, 400))
        popup.open()


class LoanCalculatorApp(App):

    def build(self):
        return LoanCalculator()


if __name__ == "__main__":
    LoanCalculatorApp().run()
