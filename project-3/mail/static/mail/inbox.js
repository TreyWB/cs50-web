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

  const heading_div = document.querySelector("#body-header")
  heading_div.innerHTML = "";
  heading_div.innerHTML = "New Email";

  // const heading_rule = document.createElement("hr");
  // heading_div.appendChild(heading_rule);

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
  const heading_div = document.querySelector("#body-header")
  heading_div.innerHTML = "";
  heading_div.innerHTML = `${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }`;

  // Clear cards before adding new ones
  document.querySelector("#emails-view").innerHTML = "";

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

        if (!email.read && mailbox !== "sent") {
          email_div.innerHTML = `
          <div class="m-0 pt-1 px-2 hover:shadow-md hover:rounded-md hover:border hover:cursor-pointer">
            <span class="flex justify-between items-center">
              <div class="text-lg font-semibold text-gray-700">${email.sender}</div>
              <div class="text-sm text-gray-500">${email.timestamp}</div>
            </span>
            <div class="mt-2">${email.subject}</div>
            <hr class="mt-2">
            </div>
        `;
        } else if (email.read && mailbox !== "sent") {
          email_div.innerHTML = `
          <div class="m-0 pt-1 px-2 hover:shadow-md hover:rounded-md hover:border bg-gray-100 rounded-lg hover:cursor-pointer">
            <span class="flex justify-between items-center">
              <div class="text-lg font-semibold text-gray-700">${email.sender}</div>
              <div class="text-sm text-gray-500">${email.timestamp}</div>
            </span>
            <div class="mt-2">${email.subject}</div>
            <hr class="mt-2">
            </div>
        `;
        } else {
          email_div.innerHTML = `
          <div class="m-0 pt-1 px-2 hover:shadow-md hover:rounded-md hover:border hover:cursor-pointer">
            <span class="flex justify-between items-center">
              <div class="text-lg font-semibold text-gray-700">${email.sender}</div>
              <div class="text-sm text-gray-500">${email.timestamp}</div>
            </span>
            <div class="mt-2">${email.subject}</div>
            <hr class="mt-2">
            </div>
        `;
        }
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

      // Set body heading
      const heading_div = document.querySelector("#body-header")
      heading_div.innerHTML = "";
      heading_div.innerHTML = `${data.subject}`;

      // ====================
      //   DISPLAY BUTTONS
      // ====================

      // If email is in sent mailbox, hide buttons
      const user_email = document.querySelector("#my-email").innerHTML;
      if (data.sender !== user_email) {
        const buttons_div = document.createElement("div");
        buttons_div.classList.add("bg-gray-600", "mt-0", "mb-0", "flex", "space-x-4", "items-center", "justify-between", "w-full");
        document.querySelector("#message-view").appendChild(buttons_div);


        // Center Buttons Container (Archive & Unread)
        const center_buttons_container = document.createElement("div");
        center_buttons_container.classList.add("flex", "items-center", "space-x-3");


        // Back button container
        const back_button_container = document.createElement("div");
        back_button_container.classList.add("relative", "inline-block"); // Set the container to relative

        // Back button
        const back_button = document.createElement("button");
        back_button.innerHTML = `
          <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12l4-4m-4 4 4 4"/>
          </svg>
        `;
        back_button.classList.add("back-button", "hover:bg-gray-500", "rounded-xl", "p-1", "ml-1");
        back_button.onclick = () => {
          if (data.archived) {
            load_mailbox("archive");
          } else {
            load_mailbox("inbox");
          }
        };

        // Tooltip label
        const tooltip = document.createElement("span");
        tooltip.classList.add(
          "invisible", 
          "opacity-0",
          "absolute", 
          "left-1/2", // Center the tooltip horizontally relative to the button
          "transform", 
          "-translate-x-1/2", // Adjust so it's perfectly centered
          "mt-9", // Margin above the tooltip
          "text-xs", 
          "bg-gray-800", 
          "text-white", 
          "rounded", 
          "px-2", 
          "py-1", 
          "transition-opacity", 
          "duration-200", 
          "whitespace-nowrap"
        );
        tooltip.innerText = "Go Back";

        back_button_container.onmouseenter = () => {
          tooltip.classList.remove("invisible", "opacity-0");
          tooltip.classList.add("visible", "opacity-100");
        };
        back_button_container.onmouseleave = () => {
          tooltip.classList.remove("visible", "opacity-100");
          tooltip.classList.add("invisible", "opacity-0");
        };
        back_button_container.appendChild(back_button);
        back_button_container.appendChild(tooltip);
        buttons_div.appendChild(back_button_container);


        // Unread button container
        const unread_button_container = document.createElement("div");
        unread_button_container.classList.add("relative", "inline-block"); // Set the container to relative

        // Unread button
        const unread_button = document.createElement("button");
        unread_button.innerHTML = `
          <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="m3.5 5.5 7.893 6.036a1 1 0 0 0 1.214 0L20.5 5.5M4 19h16a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1Z"/>
          </svg>
        `;
        unread_button.classList.add("unread-button", "hover:bg-gray-500", "rounded-xl", "p-1");
        unread_button.onclick = () => {
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

        // Tooltip label
        const unread_tooltip = document.createElement("span");
        unread_tooltip.classList.add(
          "invisible", 
          "opacity-0", 
          "absolute", 
          "left-1/2", // Center the tooltip horizontally relative to the button
          "transform", 
          "-translate-x-1/2", // Adjust so it's perfectly centered
          "mt-9", // Add margin to move the tooltip further down from the button
          "text-xs", 
          "bg-gray-800", 
          "text-white", 
          "rounded", 
          "px-2", 
          "py-1", 
          "transition-opacity", 
          "duration-200", 
          "whitespace-nowrap"
        );
        unread_tooltip.innerText = "Mark as Unread";

        unread_button_container.onmouseenter = () => {
          unread_tooltip.classList.remove("invisible", "opacity-0");
          unread_tooltip.classList.add("visible", "opacity-100");
        };
        unread_button_container.onmouseleave = () => {
          unread_tooltip.classList.remove("visible", "opacity-100");
          unread_tooltip.classList.add("invisible", "opacity-0");
        };
        unread_button_container.appendChild(unread_button);
        unread_button_container.appendChild(unread_tooltip);
        center_buttons_container.appendChild(unread_button_container);


        // Archive-Unarchive Container
        if (!data.archived) {

          // Archive button container
          const archive_button_container = document.createElement("div");
          archive_button_container.classList.add("relative", "inline-block");

          // Archive button
          const archive_button = document.createElement("button");
          archive_button.innerHTML = `
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11v5m0 0 2-2m-2 2-2-2M3 6v1a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1Zm2 2v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8H5Z"/>
            </svg>
          `;
          archive_button.classList.add("archive-button", "hover:bg-gray-500", "rounded-xl", "p-1");
          archive_button.onclick = () => {
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

                // Redirect to inbox view
                load_mailbox("inbox");
              } else {
                console.log("Error archiving email");
              }
            });
          };

          // Tooltip for archive button
          const archive_tooltip = document.createElement("span");
          archive_tooltip.classList.add(
            "invisible", 
            "opacity-0", 
            "absolute", 
            "left-1/2", 
            "transform", 
            "-translate-x-1/2", 
            "mt-9", 
            "text-xs", 
            "bg-gray-800", 
            "text-white", 
            "rounded", 
            "px-2", 
            "py-1", 
            "transition-opacity", 
            "duration-200", 
            "whitespace-nowrap"
          );
          archive_tooltip.innerText = "Archive";

          archive_button_container.onmouseenter = () => {
            archive_tooltip.classList.remove("invisible", "opacity-0");
            archive_tooltip.classList.add("visible", "opacity-100");
          };
          archive_button_container.onmouseleave = () => {
            archive_tooltip.classList.remove("visible", "opacity-100");
            archive_tooltip.classList.add("invisible", "opacity-0");
          };
          archive_button_container.appendChild(archive_button);
          archive_button_container.appendChild(archive_tooltip);
          center_buttons_container.appendChild(archive_button_container);

          // Unarchive button container
        } else if (data.archived) {
          const unarchive_button_container = document.createElement("div");
          unarchive_button_container.classList.add("relative", "inline-block");

          // Unarchive button
          const archive_button = document.createElement("button");
          archive_button.innerHTML = `
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linejoin="round" stroke-width="2" d="M10 12v1h4v-1m4 7H6a1 1 0 0 1-1-1V9h14v9a1 1 0 0 1-1 1ZM4 5h16a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/>
            </svg>
          `;
          archive_button.classList.add("unarchive-button", "hover:bg-gray-500", "rounded-xl", "p-1");
          archive_button.onclick = () => {
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
                load_mailbox("inbox");
              } else {
                console.log("Error removing email from archive");
              }
            });
          };

          // Tooltip for unarchive button
          const unarchive_tooltip = document.createElement("span");
          unarchive_tooltip.classList.add(
            "invisible", 
            "opacity-0", 
            "absolute", 
            "left-1/2", 
            "transform", 
            "-translate-x-1/2", 
            "mt-9", 
            "text-xs", 
            "bg-gray-800", 
            "text-white", 
            "rounded", 
            "px-2", 
            "py-1", 
            "transition-opacity", 
            "duration-200", 
            "whitespace-nowrap"
          );
          unarchive_tooltip.innerText = "Remove from Archive";

          unarchive_button_container.onmouseenter = () => {
            unarchive_tooltip.classList.remove("invisible", "opacity-0");
            unarchive_tooltip.classList.add("visible", "opacity-100");
          };
          unarchive_button_container.onmouseleave = () => {
            unarchive_tooltip.classList.remove("visible", "opacity-100");
            unarchive_tooltip.classList.add("invisible", "opacity-0");
          };
          unarchive_button_container.appendChild(archive_button);
          unarchive_button_container.appendChild(unarchive_tooltip);
          center_buttons_container.appendChild(unarchive_button_container);

        } else {
          console.log("Error getting archive status on:");
          console.log(data);
        }

        // Apply center buttons container
        buttons_div.appendChild(center_buttons_container);

        // Reply button container
        const reply_button_container = document.createElement("div");
        reply_button_container.classList.add("relative", "inline-block", "ml-auto", "pr-1");

        // Reply button
        const reply_button = document.createElement("button");
        reply_button.innerHTML = `
          <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.5 8.046H11V6.119c0-.921-.9-1.446-1.524-.894l-5.108 4.49a1.2 1.2 0 0 0 0 1.739l5.108 4.49c.624.556 1.524.027 1.524-.893v-1.928h2a3.023 3.023 0 0 1 3 3.046V19a5.593 5.593 0 0 0-1.5-10.954Z"/>
          </svg>
        `;
        reply_button.classList.add("reply-button", "hover:bg-gray-500", "rounded-xl", "p-1");
        reply_button.onclick = () => {
          console.log("Reply button clicked");
          reply_email(email_id);
        };

        // Tooltip for reply button
        const reply_tooltip = document.createElement("span");
        reply_tooltip.classList.add(
          "invisible", 
          "opacity-0", 
          "absolute", 
          "left-1/2", 
          "transform", 
          "-translate-x-1/2", 
          "mt-9", 
          "text-xs", 
          "bg-gray-800", 
          "text-white", 
          "rounded", 
          "px-2", 
          "py-1", 
          "transition-opacity", 
          "duration-200", 
          "whitespace-nowrap"
        );
        reply_tooltip.innerText = "Reply";

        reply_button_container.onmouseenter = () => {
          reply_tooltip.classList.remove("invisible", "opacity-0");
          reply_tooltip.classList.add("visible", "opacity-100");
        };
        reply_button_container.onmouseleave = () => {
          reply_tooltip.classList.remove("visible", "opacity-100");
          reply_tooltip.classList.add("invisible", "opacity-0");
        };
        reply_button_container.appendChild(reply_button);
        reply_button_container.appendChild(reply_tooltip);
        buttons_div.appendChild(reply_button_container);
      }

      // ====================
      // DISPLAY EMAIL DATA
      // ====================
      const email_div = document.createElement("div");
      email_div.classList.add("text-left", "bg-gray-100", "p-2");
      email_div.id = "data-container";
      email_div.innerHTML = `
        <div id="header">
          <div class="flex justify-between items-start">
            <div>
              <div class="text-gray-600 text-sm">From:</div>
              <div class="text-black ml-2">${data.sender}</div>
            </div>
            <div class="text-gray-600 text-sm">${data.timestamp}</div>
          </div>
          <div id="recipients">
            <div class="text-gray-600 text-sm">To:</div>
            <div class="text-black ml-2">${data.recipients}</div>
          </div>
          <div id="subject">
            <div class="text-gray-600 text-sm">Subject:</div>
            <div class="ml-2">${data.subject}</div>
          </div>
          </div>
          <br>
        <div id="body" class="break-words whitespace-pre-wrap">${data.body}</div>`;
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
  const heading_div = document.querySelector("#body-header")
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
      "\n-------------------------------------------------------------------------------------------------------------------\n";
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
