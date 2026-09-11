import { formatExpenseDate } from "./utils.js";
let allExpenses = [];

async function loadAllExpenses() {
    try {
        const response = await fetch("/expenses");
        const expenses = await response.json();

        allExpenses = expenses;
        displayExpenses(allExpenses);

    } catch (error) {
        console.error("Error loading expenses:", error);
    }
}

function displayExpenses(expenses) {
    const expensesList = document.getElementById("all-expenses-list");
    const emptyState = document.getElementById("empty-state");

    expensesList.innerHTML = "";

    if (expenses.length === 0) {
        emptyState.style.display = "block";
    } else {
        emptyState.style.display = "none";
    }
   
    expenses.forEach(function (expense) {
        const expenseItem = document.createElement("div");
        expenseItem.classList.add("expense-item");


        // Category
        const categoryElement = document.createElement("span");
        categoryElement.classList.add("category-tag");

        const categoryClass = "category-" + expense.category.toLowerCase();
        categoryElement.classList.add(categoryClass);
        categoryElement.textContent = expense.category;
        
        // Note
        const noteElement = document.createElement("span");
        noteElement.classList.add("expense-note");
        noteElement.textContent = expense.note;
        
        // Amount
        const amountElement = document.createElement("span");
        amountElement.classList.add("expense-amount");
        amountElement.textContent = `₹ ${expense.amount}`;
        
        // Date
        const dateElement = document.createElement("span");
        dateElement.classList.add("expense-date");
        dateElement.textContent = formatExpenseDate(expense.date);

        //Update and Delete button
        const actionsElement = document.createElement("div");
        actionsElement.classList.add("expense-actions");

        const editButton = document.createElement("button");
        editButton.classList.add("edit-expense-btn");
        editButton.textContent = "Edit";
        editButton.addEventListener("click", function () {
            createEditCard(expense);
        });
        
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("delete-expense-btn");
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function () {
            deleteExpense(expense.id);
        });

        actionsElement.appendChild(editButton);
        actionsElement.appendChild(deleteButton);

        expenseItem.appendChild(categoryElement);
        expenseItem.appendChild(noteElement);
        expenseItem.appendChild(amountElement);
        expenseItem.appendChild(dateElement);

        expensesList.appendChild(expenseItem);
        expenseItem.appendChild(actionsElement);
    });

}

const categoryFilter = document.getElementById("category-filter");
categoryFilter.addEventListener("change", function () {

    const selectedCategory = categoryFilter.value;
    if (selectedCategory === "all") {
        displayExpenses(allExpenses);
    } else {
        const filteredExpenses = allExpenses.filter(function (expense) {
            return expense.category === selectedCategory;
        });

        displayExpenses(filteredExpenses);

    }
});

async function deleteExpense(id) {
    try {
        const response = await fetch(`/expenses/${id}`, {
            method: "DELETE"
        });

        const data = await response.json();
        if (!response.ok) {
            showActionMessage(data.message, "error");
            return;
        }
        
        showActionMessage(data.message);
        loadAllExpenses();
    } catch (error) {
        console.error("Error deleting expense:", error);
        showActionMessage("Something went wrong. Please try again.", "error");
    }
}


function createEditCard(expense) {
    const editCard = document.createElement("div");
    editCard.classList.add("edit-card");

    // Heading
    const heading = document.createElement("h2");
    heading.textContent = "Edit Expense";

    // Amount
    const amountLabel = document.createElement("label");
    amountLabel.textContent = "Amount";

    const amountInput = document.createElement("input");
    amountInput.type = "number";
    amountInput.value = expense.amount;

    // Category
    const categoryLabel = document.createElement("label");
    categoryLabel.textContent = "Category";

    const categorySelect = document.createElement("select");

    const categories = [
        "Food",
        "Transport",
        "Groceries",
        "Shopping",
        "Entertainment",
        "Bills",
        "Gifts",
        "Health",
        "Rent",
        "Education",
        "Other"
    ];

    categories.forEach(function (category) {
        const option = document.createElement("option");

        option.value = category;
        option.textContent = category;

        if (category === expense.category) {
            option.selected = true;
        }

        categorySelect.appendChild(option);
    });

    // Note
    const noteLabel = document.createElement("label");
    noteLabel.textContent = "Note";

    const noteInput = document.createElement("input");
    noteInput.type = "text";
    noteInput.value = expense.note || "";

    // Actions
    const actions = document.createElement("div");
    actions.classList.add("edit-card-actions");

    const updateButton = document.createElement("button");
    updateButton.textContent = "Update Expense";
    updateButton.classList.add("update-expense-btn");
    updateButton.addEventListener("click", function () {
        updateExpense(
            expense.id,
            amountInput.value,
            categorySelect.value,
            noteInput.value
        );
    });

    const cancelButton = document.createElement("button");
    cancelButton.textContent = "Cancel";
    cancelButton.classList.add("cancel-edit-btn");
    cancelButton.addEventListener("click", function () {
        editCard.remove();
    });

    actions.appendChild(updateButton);
    actions.appendChild(cancelButton);

    // Add everything to card
    editCard.appendChild(heading);

    editCard.appendChild(amountLabel);
    editCard.appendChild(amountInput);

    editCard.appendChild(categoryLabel);
    editCard.appendChild(categorySelect);

    editCard.appendChild(noteLabel);
    editCard.appendChild(noteInput);

    editCard.appendChild(actions);

    // Add card to page
    document.body.appendChild(editCard);

}

async function updateExpense(id, amount, category, note) {
    try {
        const response = await fetch(`/expenses/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                amount: Number(amount),
                category: category,
                note: note
            })
        });

        const data = await response.json();
        
        const actionMessage = document.getElementById("action-message");
        actionMessage.textContent = data.message;
        actionMessage.style.display = "block";

        if (!response.ok) {
            showActionMessage(data.message, "error");
            return;
        }
        
        showActionMessage(data.message);
        loadAllExpenses(); // Loads all updated expenses
        
        document.querySelector(".edit-card").remove(); // Closes edit card

    } catch (error) {
        console.error("Error updating expense:", error);
        showActionMessage("Something went wrong. Please try again.", "error");
    }
}
loadAllExpenses();

function showActionMessage(message, type = "success") {
    const actionMessage = document.getElementById("action-message");

    actionMessage.textContent = message;
    actionMessage.className = `action-message ${type}`;
    actionMessage.style.display = "block";

    setTimeout(function () {
        actionMessage.style.display = "none";
    }, 3000);
}