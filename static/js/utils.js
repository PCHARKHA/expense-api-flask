export function formatExpenseDate(expenseDate) {
    const today = new Date();
    const expenseDateObject = new Date(expenseDate);

    today.setHours(0, 0, 0, 0);
    expenseDateObject.setHours(0, 0, 0, 0);

    const differenceInMilliseconds = today - expenseDateObject;
    const differenceInDays = differenceInMilliseconds / (1000 * 60 * 60 * 24);
     
    if (differenceInDays === 0) {
        return "Today";
    }

    if (differenceInDays === 1) {
        return "Yesterday";
    }

    return `${differenceInDays} days ago`;
}

export function getAuthToken() {
    return localStorage.getItem("access_token");
}

export function handleUnauthorized() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}