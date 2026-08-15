(function () {
    const widget = document.getElementById('contact-widget');
    if (!widget) return;

    const toggle = document.getElementById('contact-toggle');
    const panel = document.getElementById('contact-panel');
    const form = document.getElementById('contact-form');
    const status = document.getElementById('contact-status');
    const submit = form.querySelector('button[type="submit"]');
    const nameInput = document.getElementById('contact-name');

    function setOpen(open, restoreFocus) {
        widget.dataset.open = String(open);
        toggle.setAttribute('aria-expanded', String(open));
        toggle.setAttribute('aria-label', open ? 'Close contact form' : 'Open contact form');
        panel.setAttribute('aria-hidden', String(!open));

        if (open) {
            window.setTimeout(function () { nameInput.focus(); }, 180);
        } else if (restoreFocus) {
            toggle.focus();
        }
    }

    toggle.addEventListener('click', function () {
        setOpen(widget.dataset.open !== 'true', false);
    });

    document.addEventListener('click', function (event) {
        if (widget.dataset.open === 'true' && !widget.contains(event.target)) {
            setOpen(false, false);
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && widget.dataset.open === 'true') {
            setOpen(false, true);
        }
    });

    form.addEventListener('submit', async function (event) {
        if (!window.fetch) return;

        event.preventDefault();
        status.textContent = '';
        status.removeAttribute('data-state');
        submit.disabled = true;
        submit.textContent = 'Sending…';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { Accept: 'application/json' }
            });

            if (!response.ok) {
                let message = 'Your message could not be sent. Please try again.';
                try {
                    const data = await response.json();
                    if (data.errors && data.errors.length) {
                        message = data.errors.map(function (error) { return error.message; }).join(' ');
                    }
                } catch (ignore) {}
                throw new Error(message);
            }

            form.reset();
            status.dataset.state = 'success';
            status.textContent = 'Thanks—your message has been sent.';
        } catch (error) {
            status.dataset.state = 'error';
            status.textContent = error.message || 'Your message could not be sent. Please try again.';
        } finally {
            submit.disabled = false;
            submit.textContent = 'Send Message';
        }
    });
})();
