import { handleUnauthorized } from "./utils.js";

async function loadHighestSpendingCategory() {
    try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("/expenses/insights/highest-category", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        const data = await response.json();

        if (!response.ok) {
            console.error("Backend error:", data);
            return;
        }

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
        const token = localStorage.getItem("access_token");
        const response = await fetch("/expenses/insights/daily-average", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            console.error("Backend error:", data);
            return;
        }

        document.getElementById("daily-average").textContent =`₹ ${data.daily_average} / day`;

    } catch (error) {
        console.error("Error loading daily average:", error);
    }
}

async function loadMonthlyComparison() {
    try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(
            "/expenses/insights/monthly-compare",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            console.error("Backend error:", data);
            return;
        }

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
        const token = localStorage.getItem("access_token");
        const response = await fetch(
            "/expenses/insights/weekend-pattern",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {
            handleUnauthorized();
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            console.error("Backend error:", data);
            return;
        }

        // Display spending amounts
        document.getElementById("weekday-total").textContent =`₹ ${data.weekday_total}`;
        document.getElementById("weekend-total").textContent =`₹ ${data.weekend_total}`;

        // Display percentages
        document.getElementById("weekday-percentage").textContent =`${data.weekday_percentage}%`;
        document.getElementById("weekend-percentage").textContent = `${data.weekend_percentage}%`;
        
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
loadHighestSpendingCategory();
loadDailyAverage();
loadMonthlyComparison();
loadWeekendPattern();