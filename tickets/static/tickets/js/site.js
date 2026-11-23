const seatForm = document.querySelector("[data-seat-form]");

if (seatForm) {
    const inputs = [...seatForm.querySelectorAll("input[name=seats]:not(:disabled)")];
    const output = seatForm.querySelector("[data-seat-total]");
    const price = Number(seatForm.dataset.seatPrice);

    function updateSeatCount() {
        const count = inputs.filter(input => input.checked).length;
        const total = new Intl.NumberFormat("en-IN").format(count * price);
        output.value = count > 0 ? ` · ${count} selected · ₹${total} total` : "";
    }

    seatForm.addEventListener("change", event => {
        if (inputs.filter(input => input.checked).length > 6) {
            event.target.checked = false;
            output.value = " · You can choose up to six seats.";
        } else {
            updateSeatCount();
        }
    });
    updateSeatCount();
}

const featured = document.querySelector("[data-featured]");

if (featured) {
    const controls = featured.querySelector(".feature-controls");
    const buttons = [...controls.querySelectorAll("button")];
    const slides = new Map(
        [...featured.querySelectorAll(".feature-slide")].map(slide => [slide.id, slide])
    );

    controls.hidden = false;
    controls.addEventListener("click", event => {
        const selected = event.target.closest("button");
        if (!selected || selected.getAttribute("aria-pressed") === "true") {
            return;
        }
        for (const button of buttons) {
            const active = button === selected;
            button.setAttribute("aria-pressed", String(active));
            slides.get(button.getAttribute("aria-controls")).hidden = !active;
        }
    });
}
