document.getElementById('selectAll').addEventListener('change', toggleSelectAll);

function toggleSelectAll() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
        toggleActiveClass(checkbox);
    });
}

function toggleActiveClass(checkbox) {
    if (checkbox.checked) {
        checkbox.closest('.table-row').classList.add('active');
    } else {
        checkbox.closest('.table-row').classList.remove('active');
    }
}

// Add event listeners to each row checkbox to handle manual checking/unchecking
document.querySelectorAll('.row-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        toggleActiveClass(this);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll("#running-costs-tbody tr");
    rows.forEach(row => {
        const isLate = row.getAttribute("data-late") === "True";
        if (isLate) {
            row.classList.add("late-payment");
        }
    });
});
