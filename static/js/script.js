  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => el.style.display = 'none');
  }, 4000); 
function updateCaseStatus(caseId) {
  fetch(`/case-status/${caseId}/`, { cache: "no-store" })
    .then(response => response.json())
    .then(data => {
      if (data.status) {
        const badge = document.getElementById(`status-badge-${caseId}`);
        const msg = document.getElementById(`status-msg-${caseId}`);
        const status = data.status.toLowerCase();

        badge.className = "badge " + {
          "pending": "bg-warning text-dark",
          "approved": "bg-info",
          "rejected": "bg-danger",
          "delivered": "bg-success"
        }[status];

        badge.textContent = data.status;

        msg.textContent = {
          "pending": "⏳ Waiting for admin approval of your proof.",
          "approved": "✔ Your case is approved and visible to donors.",
          "rejected": "❌ Your proof was rejected. Please upload a valid document and resubmit.",
          "delivered": "🎉 Your case has been fully funded!"
        }[status];
      }

      if (data.attachments) {
        console.log("Attachments:", data.attachments);
      }
    })
    .catch(err => console.error("Error fetching case status:", err));
}

document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
      document.querySelectorAll('.alert').forEach(el => {
        let alert = new bootstrap.Alert(el);
        alert.close();
      });
    }, 3000);
  });