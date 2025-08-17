import sys, time
import serial
import lewansoul_lx16a

SERIAL_PORT = 'COM5'  # change port as necessary

try:
    ctrl = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1),
    )
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit()
    

def print_welcome():
    print("\n" + "=" * 55)
    print("    🐕 WELCOME TO THE LAIKA QUADRUPED DOG DEMO 🐕")
    print("=" * 55)
    print()
    print("Hello! Meet LAIKA, our amazing quadruped robot dog!")
    print("LAIKA is ready to demonstrate its incredible capabilities")
    print("and show you some impressive maneuvers.")
    print()
    print("During this demo, LAIKA will perform various movements")
    print("including walking, turning, balancing, and other cool")
    print("maneuvers to showcase its advanced servo control system.")
    print()
    print("🤖 Ready to see LAIKA in action?")
    print()
    print("Press ENTER to start the demo, or type EXIT to close the demo!")
    print("-" * 55)

# TODO: Add functions that each of which shows different maneuvers that LAIKA can perform.


# Main function
if __name__ == "__main__":
    # Show welcome message and prompt for demo
    print_welcome()
    
    user_choice = input().strip().lower()
    
    if user_choice != 'exit':
        print("\n🎬 Starting LAIKA Demo Sequence...")
        print("Watch as LAIKA demonstrates its capabilities!")
        print("(Demo functionality to be implemented)")
        time.sleep(2)
        print("\nDemo completed!\n")
    else:
        print("\nExiting demo...\n")
