from app.chat_engine import ask_bizzy
from app.memory.thread_state import add_message, get_thread, reset_thread
import time
from app.services.relay_analysis import analyze_for_relay



def simulate_convo(phone_number):
    print("---- New Simulated SMS Thread ----")

    while True:
        user_input = input("Client: ")
        if user_input.lower() in ("quit", "exit"):
            reset_thread(phone_number)
            break

        # adding a client message to the thread

        add_message(phone_number, "user", user_input)

        # grab the updated thread * which includes the inital message sent by the client

        messages = get_thread(phone_number)

        
        relay_result = analyze_for_relay(user_input, messages)
        print("🔎 Relay Analysis:", relay_result)

        if relay_result["sensitivity"] >= 8:
            print(f"Bizzy: {relay_result['bizzy_response']}\n")
            add_message(phone_number, "assistant", relay_result["bizzy_response"])
            continue #telling bizzy to skip the call for now and wait for Melissa's guidance


        if not messages:
            print("⚠️ No messages in thread - skipping response.")
            continue

    
        thread_prompt = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages]
        )

        if not thread_prompt.strip():
            print("⚠️ No messages yet in thread. Skipping GPT call.")
            continue

        system_prompt = "You are bizzy, a friendly AI assistant for a hairstylist. You are provided the authority to help clients select an appointment slot!"

        #first prompt sent to bizzy
        response = ask_bizzy(system_prompt, thread_prompt)

        #save bizzy's response to the memory bank

        add_message(phone_number, "assistant", response)
        
        print(f"Bizzy: {response}\n")
        time.sleep(0.2)




if __name__ == "__main__":
    simulate_convo("3234594057")

    
    '''system_prompt = "You are bizzy, a friendly AI assistant for a hairstylist. You are provided the authority to help clients select an appointment slot!"
    message = "Hi, do you have anything available on Friday or Saturday?"

    response = ask_bizzy(system_prompt, message)
    print("\n--- Bizzy 📲---")
    print(response)'''
