document.addEventListener('DOMContentLoaded', () => {
  const trigger = document.getElementById('chatbot-trigger');
  const chatbot = document.getElementById('chatbot');
  const closeBtn = document.getElementById('chatbot-close');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  // Open chatbot on trigger click
  trigger.addEventListener('click', () => {
    chatbot.classList.remove('hidden');
    trigger.classList.add('hidden');
  });

  // Close chatbot on X button click
  closeBtn.addEventListener('click', () => {
    chatbot.classList.add('hidden');
    trigger.classList.remove('hidden');
  });

  // Handle form submission
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (message) {
      const newMessage = `<div class="mb-2 text-right"><p class="inline-block p-2 rounded-lg bg-gray-700">${message}</p></div>`;
      chatMessages.innerHTML += newMessage;
      chatMessages.scrollTop = chatMessages.scrollHeight;

      // Simulate bot response (replace with actual API call if needed)
      setTimeout(() => {
        const botResponse = `<div class="mb-2 text-left"><p class="inline-block p-2 rounded-lg bg-green-600">Thanks for your message! How about starting a project with us?</p></div>`;
        chatMessages.innerHTML += botResponse;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 500);

      chatInput.value = '';
    }
  });
});