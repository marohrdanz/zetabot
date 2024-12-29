import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    system="You are Santa Clause; respone like Santa Clause.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the sky red at sunset?"
                }
            ]
        }
    ]
)
print(message.content)
print('\n--------------------------\n')
print(message.content[0].text)
