document.addEventListener("DOMContentLoaded", () => {
  // مرّ على كل عنصر فيه data-case-id
  document.querySelectorAll("[data-case-id]").forEach(el => {
    const caseId = el.dataset.caseId;

    // افتح WebSocket للـ case
    const socket = new WebSocket(
      (window.location.protocol === "https:" ? "wss://" : "ws://") +
      window.location.host +
      "/ws/case/" + caseId + "/"
    );

    // لما يوصل تحديث من السيرفر
    socket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      const status = data.status.toLowerCase();

      const badge = document.getElementById(`status-badge-${caseId}`);
      const msg = document.getElementById(`status-msg-${caseId}`);

      if (badge) {
        badge.className = "badge px-3 py-2 rounded-pill " + {
          "pending": "bg-warning text-dark",
          "approved": "bg-info",
          "rejected": "bg-danger",
          "delivered": "bg-success"
        }[status];
        badge.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
      }

      if (msg) {
        msg.textContent = {
          "pending": "⏳ Waiting for admin approval of your proof.",
          "approved": "✔ Your case is approved and visible to donors.",
          "rejected": "❌ Your proof was rejected. Please upload a valid document and resubmit.",
          "delivered": "🎉 Your case has been fully funded!"
        }[status];
      }
    };

    socket.onclose = function() {
      console.warn("WebSocket closed for case:", caseId);
    };

    socket.onerror = function(err) {
      console.error("WebSocket error:", err);
    };
  });
});
