document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
  document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
  document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // Send email on submit
  document.querySelector("#compose-form").addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#message-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  const heading_div = document.querySelector("#heading")
  heading_div.innerHTML = "";
  heading_div.innerHTML = "New Email";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}


function load_mailbox(mailbox) {  
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#message-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Load emails via API
  fetch(`emails/${mailbox}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);

      // Display emails
      data.forEach((email) => {
        const email_div = document.createElement("div");
        email_div.classList.add("email-card");
        email_div.onclick = () => {
          view_email(email.id);
        };
        email_div.innerHTML = `
          <hr>
          <div class="email-header">
            <div class="email-sender">${email.sender}</div>
            <div class="email-timestamp">${email.timestamp}</div>
            <div class="email-subject">${email.subject}</div>
          </div>`;
        document.querySelector("#emails-view").appendChild(email_div);
      });
    });
}

function view_email(email_id) {
  // Hide everything except message view
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#message-view").style.display = "block";

  // Clear the message view
  document.querySelector("#message-view").innerHTML = "";

  // Load email via API
  fetch(`emails/${email_id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("Email Data:");
      console.log(data);

      // ====================
      // DISPLAY BUTTONS
      // ====================

      // If email is in sent mailbox, hide buttons
      const user_email = document.querySelector("#my-email").innerHTML;

      if (data.sender !== user_email) {
        const buttons_div = document.createElement("div");
        buttons_div.classList.add("buttons");
        document.querySelector("#message-view").appendChild(buttons_div);

        // Unread button
        const unread_span = document.createElement("span");
        unread_span.innerHTML = "<button>Mark Unread</button>";
        unread_span.classList.add("unread-button");
        unread_span.onclick = () => {
          fetch(`emails/${email_id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              read: false,
            }),
          }).then((response) => {
            if (response.status === 204) {
              console.log("Email marked as unread");
            } else {
              console.log("Error marking email as unread");
            }
          });
        };
        buttons_div.appendChild(unread_span);

        // Archive-Unarchive button
        if (!data.archived) {
          const archive_span = document.createElement("span");
          archive_span.innerHTML = "<button>Archive</button>";
          archive_span.classList.add("archive-button");
          archive_span.onclick = () => {
            fetch(`emails/${email_id}`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                archived: true,
              }),
            }).then((response) => {
              if (response.status === 204) {
                console.log("Email archived");

                // Redirect to archive view
                load_mailbox("inbox")
              } else {
                console.log("Error archiving email");
              }
            });
          };
          buttons_div.appendChild(archive_span);
        } else if (data.archived) {
          const archive_span = document.createElement("span");
          archive_span.innerHTML = "<button>Unarchive</button>";
          archive_span.classList.add("unarchive-button");
          archive_span.onclick = () => {
            fetch(`emails/${email_id}`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                archived: false,
              }),
            }).then((response) => {
              if (response.status === 204) {
                console.log("Email removed from archive");

                // Redirect to inbox view
                load_mailbox("inbox")
              } else {
                console.log("Error removing email from archive");
              }
            });
          };
          buttons_div.appendChild(archive_span);
        } else {
          console.log("Error getting archive status on:");
          console.log(data);
        }

        // Reply button
        const reply_span = document.createElement("span");
        reply_span.innerHTML = "<button>Reply</button>";
        reply_span.classList.add("reply-button");
        reply_span.onclick = () => {
          console.log("Reply button clicked");
          reply_email(email_id);
        };
        buttons_div.appendChild(reply_span);
      }

      // ====================
      // DISPLAY EMAIL DATA
      // ====================
      const email_div = document.createElement("div");
      email_div.classList.add("email");
      email_div.innerHTML = `
        <div class="email-header">
          <div class="email-sender">From: ${data.sender}</div>
          <div class="email-sender">To: ${data.recipients}</div>
          <div class="email-timestamp">${data.timestamp}</div>
          <div class="email-subject">${data.subject}</div>
          </div>
          <br>
        <div class="email-body" style="white-space: pre-wrap;">${data.body}</div>`;
      document.querySelector("#message-view").appendChild(email_div);
    });

  // Mark email as read
  fetch(`emails/${email_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      read: true,
    }),
  }).then((response) => {
    if (response.status === 204) {
      console.log("Email marked as read");
    } else {
      console.log("Error marking email as read");
    }
  });
}

function reply_email(email_id) {
  // Display only compose view
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#message-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Change heading
  const heading_div = document.querySelector("#heading")
  heading_div.innerHTML = "";
  heading_div.innerHTML = "Reply";

  // Get email data
  fetch(`emails/${email_id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("Email Data:");
      console.log(data);

      // Populate fields
      const recipients_field = document.querySelector("#compose-recipients");
      recipients_field.value = data.sender;

      const subject_field = document.querySelector("#compose-subject");
      let subject_data = data.subject;
      subject_data = "Re: " + subject_data;
      subject_field.value = subject_data;

      const body_field = document.querySelector("#compose-body");
      let body_data = data.body;
      body_data = `On ${data.timestamp} ` + `${data.sender} wrote:\n` + body_data + 
      "\n-------------------------\n";
      body_field.value = body_data;
    });
}

function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Send email via API
  fetch("emails", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Email sent:", data);
      load_mailbox("inbox");
    });
}
