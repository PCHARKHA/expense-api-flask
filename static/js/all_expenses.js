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

        expenseItem.appendChild(categoryElement);
        expenseItem.appendChild(noteElement);
        expenseItem.appendChild(amountElement);
        expenseItem.appendChild(dateElement);

        expensesList.appendChild(expenseItem);
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

loadAllExpenses();