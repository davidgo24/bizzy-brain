from app.chat_engine import ask_bizzy
from app.memory.thread_state import add_message, get_thread, reset_thread
import time

def simulate_convo(phone_number="323-450-2012"):
    print("---- New Simulated SMS Thread ----")

    while True:
        user_input = input("Client: ")
        if user_input.lower() in ("quit", "exit"):
            reset_thread(phone_number)
            break

        # adding a client message to the thread

        add_message(phone_number, "user", user_input)

        # constructing a full thread prompt

        messages = get_thread(phone_number)

        thread_prompt = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages]
        )
        
        system_prompt = "You are bizzy, a friendly AI assistant for a hairstylist. You are provided the authority to help clients select an appointment slot!"


        response = ask_bizzy(system_prompt, thread_prompt)

        #add bizzy response to memory

        add_message(phone_number, "assistant", response)
        
        print(f"Bizzy: {response}\n")
        time.sleep(0.2)




if __name__ == "__main__":
    simulate_convo()

    
    '''system_prompt = "You are bizzy, a friendly AI assistant for a hairstylist. You are provided the authority to help clients select an appointment slot!"
    message = "Hi, do you have anything available on Friday or Saturday?"

    response = ask_bizzy(system_prompt, message)
    print("\n--- Bizzy 📲---")
    print(response)'''
