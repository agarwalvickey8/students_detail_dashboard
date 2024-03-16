document.addEventListener("DOMContentLoaded", function() {
    const studentDetailsCheckbox = document.querySelector("#action-toggle");
    const studentCheckboxes = document.querySelectorAll("input[name=_selected_action]");

    if (studentDetailsCheckbox && studentCheckboxes.length > 1) {
        studentDetailsCheckbox.addEventListener("change", function() {
            const isChecked = this.checked;
            studentCheckboxes.forEach(function(checkbox) {
                checkbox.checked = isChecked;
            });
        });
    }
});
