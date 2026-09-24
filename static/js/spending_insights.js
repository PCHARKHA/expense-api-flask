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

loadHighestSpendingCategory();
loadDailyAverage();