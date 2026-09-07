const amountDisplay = document.getElementById("amount-display");
const amountValue = document.getElementById("amount-value");
const numericKeypad = document.getElementById("numeric-keypad");
const keypadKeys = document.querySelectorAll(".keypad-key");

const expenseForm = document.getElementById("expense-form");
const categorySelect = document.getElementById("category-select");
const expenseNote = document.getElementById("expense-note");
const formMessage = document.getElementById("form-message");

let currentAmount = "0";

amountDisplay.addEventListener("click", function () {
    numericKeypad.classList.toggle("active");
});

keypadKeys.forEach(function(key){
    key.addEventListener("click", function () {
        const keyValue = key.dataset.key;
        //Logic for backspace button
        if (keyValue === "clear") {
            currentAmount = currentAmount.slice(0, -1);

            if (currentAmount === "") {
                currentAmount = "0";
            }
        }

        // Logic for decimal or point
        else if (keyValue === ".") {
            if (!currentAmount.includes(".")) {
                currentAmount += ".";
            }
        }
        // Adding amount
        else {
            if (currentAmount === "0") {
                currentAmount = keyValue;
            } else {
                currentAmount += keyValue;
            }
        }

        amountValue.textContent = currentAmount;
    });
});


expenseForm.addEventListener("submit", function (event) {
    event.preventDefault();
    
    formMessage.textContent = "";
    formMessage.className = "form-message";

    const amount = currentAmount;
    const category = categorySelect.value;
    const note = expenseNote.value;

    const expenseData = {
        amount: Number(amount),
        category: category,
        note: note
    };

    if (!amount || amount <= 0) {
        formMessage.textContent = "Please enter a valid amount.";
        formMessage.className = "form-message error";
        return;
    }

    if (category === "") {
        formMessage.textContent = "Please select a category.";
        formMessage.className = "form-message error";
        return;
    }
    
    sendToBackend(expenseData);
});

function sendToBackend(expenseData){
    fetch("/expenses", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(expenseData)
    })
        .then(function (response) {
            return response.json().then(function (data) {
                return {
                    ok: response.ok,
                    data: data
                };
            });
        })
        .then(function (result) {
    
            if (result.ok) {
                formMessage.textContent = result.data.message;
                formMessage.className = "form-message success";
    
                currentAmount = "0";
                amountValue.textContent = currentAmount;
    
                categorySelect.value = "";
                expenseNote.value = "";
    
                numericKeypad.classList.remove("active");

                setTimeout(function () {
                    formMessage.textContent = "";
                    formMessage.className = "form-message";
                }, 3000);
            } else {
                formMessage.textContent = result.data.message;
                formMessage.className = "form-message error";
            }
    
        })
        .catch(function (error) {
            formMessage.textContent = "Something went wrong. Please try again.";
            formMessage.className = "form-message error";
    
            console.error("Error:", error);
        });
}