document.addEventListener("DOMContentLoaded", () => {
    const primaryToggleInput =
        document.getElementById("pst-primary-sidebar-checkbox") ||
        document.querySelector("input.sidebar-toggle");

    if (!primaryToggleInput) {
        return;
    }

    const targetId =
        primaryToggleInput.id && primaryToggleInput.id.trim().length > 0
            ? primaryToggleInput.id
            : "pst-primary-sidebar-checkbox";

    const relatedLabels = document.querySelectorAll(
        'label.sidebar-toggle.primary-toggle,' +
            'label.overlay.overlay-primary,' +
            `label[for="${targetId}"]`
    );

    relatedLabels.forEach((label) => {
        if (label.getAttribute("for") !== targetId) {
            label.setAttribute("for", targetId);
        }
    });
});

