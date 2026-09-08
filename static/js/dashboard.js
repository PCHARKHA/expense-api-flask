import { formatExpenseDate } from "./utils.js";
async function loadDashboard() {
    try {
        const response = await fetch("/expenses");
        const expenses = await response.json();
    
        calculateSummary(expenses);
        displayRecentExpenses(expenses);
    
        }catch (error) {
            console.error("Error loading dashboard:", error);
        }
    
    }

function calculateSummary(expenses){
    const todayTotalElement = document.getElementById("today-total");
    const weekTotalElement = document.getElementById("week-total");
    const monthTotalElement = document.getElementById("month-total");

    const today = new Date();

    let todayTotal = 0;
    let weekTotal = 0;
    let monthTotal = 0;

    const startOfWeek = new Date(today);
    const day = today.getDay();
    startOfWeek.setDate(today.getDate() - day);
    startOfWeek.setHours(0, 0, 0, 0);
    
    expenses.forEach(function (expense) {
        const expenseDate = expense.date;
        const todayDate = today.toISOString().split("T")[0];

        const expenseDateObject = new Date(expense.date);

        const expenseMonth = expenseDateObject.getMonth();
        const expenseYear = expenseDateObject.getFullYear();

        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();

        if (expenseDate === todayDate) {
                todayTotal = todayTotal + expense.amount;
        }

        // This week's expense
        if (expenseDateObject >= startOfWeek && expenseDateObject <= today) {
                 weekTotal = weekTotal + expense.amount;
        }
        //This months's expense
        if (expenseMonth === currentMonth && expenseYear === currentYear) {
                monthTotal = monthTotal + expense.amount;
            }
        });
        
        todayTotalElement.textContent = `₹ ${todayTotal}`;
        weekTotalElement.textContent = `₹ ${weekTotal}`;
        monthTotalElement.textContent = `₹ ${monthTotal}`;
}
//Working on add expense button
const addExpenseButton = document.getElementById("add-expense-btn");

addExpenseButton.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/add-expense";

});


function displayRecentExpenses(expenses){
    const expenseList = document.getElementById("expense-list");
    expenseList.innerHTML = "";

    const recentExpenses = expenses.slice(-5).reverse();

    recentExpenses.forEach(function (expense) {
        const expenseItem = document.createElement("div");
        expenseItem.classList.add("expense-item");

        const categoryElement = document.createElement("span");
        categoryElement.classList.add("category-tag");
        // Code to add category-specific css
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

        //Appending to expenseItem
        expenseItem.appendChild(categoryElement);
        expenseItem.appendChild(noteElement);
        expenseItem.appendChild(amountElement);
        expenseItem.appendChild(dateElement);

        expenseList.appendChild(expenseItem);
    });
}

// const viewAllLink = document.getElementById("view-all-link");
// viewAllLink.addEventListener("click", function (event) {
//     event.preventDefault();
//     window.location.href = "/all_expenses";
// });

loadDashboard();