document.addEventListener('DOMContentLoaded', function () {
    let incomeIdToDelete;

    // Attach click event to all delete buttons
    document.querySelectorAll('.delete-button').forEach(function (deleteButton) {
        deleteButton.addEventListener('click', function (event) {
            event.preventDefault();
            incomeIdToDelete = this.getAttribute('data-income-id');
        });
    });

    // Handle confirm delete button click
    document.getElementById('confirmDeleteButton').addEventListener('click', function () {
        if (incomeIdToDelete) {
            fetch(`/incomes/${incomeIdToDelete}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (response.ok) {
                        $('#deleteIncomeModal').modal('hide');
                        location.reload();
                    } else {
                        alert('Error deleting income');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error deleting income');
                });
        }
    });

    // Function to get CSRF token (needed for Django's CSRF protection)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
