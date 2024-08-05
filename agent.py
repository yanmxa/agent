
class Agent:
  def __init__(self, client, system):
    self.client = client
    self.system = system
    self.messages = []
    if self.system:
      self.messages.append({"role": "system", "content": self.system})
      
  def __call__(self, message=""):
    if message:
      self.messages.append({"role": "user", "content": message})
    result = self.execute()
    self.messages.append({"role": "assistant", "content": result})
    return result

  def execute(self):
    chat_completion = self.client.chat.completions.create(
      messages=self.messages,
      model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content
