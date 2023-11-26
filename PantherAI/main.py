import assistantsfunctions
from assistants import client

# if "NEWCHANGE" in os.environ:
start = False

assistant = client.beta.assistants.retrieve(
  assistant_id="asst_qDS5qAI2qmbD6dV4xwyXSwiw"
)

# if __name__ == "__main__":
#   if start:
#     file = client.files.create(file=open("jls.txt", "rb"), purpose='assistants')
#     assistant = client.beta.assistants.create(
#       name="PantherAI",
#       instructions="As PantherAI, your role is to provide brief and concise information about Jane Lathrop Stanford Middle School's lunch menu, schedule, calendar, events, and news. When asked about the lunch menu, give a quick overview of the day's options or the weekly menu, as requested. For schedule inquiries, provide key times and any special schedule details without excessive elaboration. In discussions about the school calendar and events, offer essential dates and information about upcoming activities.",
#       tools=[{"type": "retrieval"}, assistantsfunctions.menufunc],
#       model="gpt-3.5-turbo-1106",
#       file_ids=[file.id]
#     )
#   else:
#     assistant = client.beta.assistants.retrieve(
#       assistant_id="asst_qDS5qAI2qmbD6dV4xwyXSwiw"
#     )