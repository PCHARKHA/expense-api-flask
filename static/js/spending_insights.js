import { apiRequest } from "./utils.js";

async function loadHighestSpendingCategory() {
    try {
        const result = await apiRequest("/expenses/insights/highest-category");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        document.getElementById("highest-category").textContent =data.category;
        document.getElementById("highest-category-amount").textContent =`₹ ${data.amount}`;
        document.getElementById("highest-category-percentage").textContent =
                                `${data.percentage}% of your monthly spending`;

    } catch (error) {
        console.error("Error loading highest spending category:", error);
    }
}

async function loadDailyAverage() {
    try {
        const result = await apiRequest("/expenses/insights/daily-average");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        document.getElementById("daily-average").textContent =`₹ ${data.daily_average} / day`;

    } catch (error) {
        console.error("Error loading daily average:", error);
    }
}

async function loadMonthlyComparison() {
    try {
        const result = await apiRequest("/expenses/insights/monthly-compare");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        // Display current and previous month totals
        document.getElementById("current-month-total").textContent =`₹ ${data.current_total}`;
        document.getElementById("previous-month-total").textContent =`₹ ${data.previous_total}`;
        
        // Display percentage comparison
        const comparisonElement = document.getElementById("monthly-comparison");

        if (data.percentage_change === null) {
            comparisonElement.textContent = "No spending data from last month";

        } else if (data.status === "increased") {
            comparisonElement.textContent = `↑ ${data.percentage_change}% vs last month`;

        } else if (data.status === "decreased") {
            comparisonElement.textContent = `↓ ${Math.abs(data.percentage_change)}% vs last month`;
        } else {
            comparisonElement.textContent = "Same spending as last month";
        }
    } catch (error) {
        console.error("Error loading monthly comparison:", error);
    }
}

async function loadWeekendPattern() {
    try {
        const result = await apiRequest("/expenses/insights/weekend-pattern");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        // Display spending amounts
        document.getElementById("weekday-total").textContent =`₹ ${data.weekday_total}`;
        document.getElementById("weekend-total").textContent =`₹ ${data.weekend_total}`;

        // Display percentages
        document.getElementById("weekday-percentage").textContent =`${data.weekday_percentage}%`;
        document.getElementById("weekend-percentage").textContent = `${data.weekend_percentage}%`;
        document.getElementById("weekday-bar-fill").style.width = `${data.weekday_percentage}%`;
        document.getElementById("weekend-bar-fill").style.width = `${data.weekend_percentage}%`;
        
        // Display overall pattern
        const patternElement = document.getElementById("spending-pattern");

        if (data.pattern === "weekend") {
            patternElement.textContent =
                `You spend more on weekends — ${data.weekend_percentage}% of your spending happens on weekends.`;

        } else if (data.pattern === "weekday") {
            patternElement.textContent =
                `You spend more on weekdays — ${data.weekday_percentage}% of your spending happens on weekdays.`;

        } else {
            patternElement.textContent = "Your weekday and weekend spending are equal.";
        }
    } catch (error) {
        console.error("Error loading weekend spending pattern:", error);
    }
}

async function loadSmallExpenses() {
    try {
        const result = await apiRequest("/expenses/insights/small-expenses");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        document.getElementById("small-expense-count").textContent = `${data.count} small expenses`;
        document.getElementById("small-expense-total").textContent = `₹ ${data.total}`;
    } catch (error) {
        console.error("Error loading small expenses:", error);
    }
}

async function loadNoSpendDays() {
    try {
        const result = await apiRequest("/expenses/insights/no-spend-days");
        if (!result) return;

        if (!result.ok) {
            console.error("Backend error:", result.data);
            return;
        }

        const data = result.data;

        document.getElementById("no-spend-days").textContent =  `${data.no_spend_days} days`;
    } catch (error) {
        console.error("Error loading no-spend days:", error);
    }
}

loadHighestSpendingCategory();
loadDailyAverage();
loadMonthlyComparison();
loadWeekendPattern();
loadSmallExpenses();
loadNoSpendDays();