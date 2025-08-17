import sys, time
import serial
import lewansoul_lx16a

SERIAL_PORT = 'COM5'  # change port as necessary

ctrl = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1),
)

def print_help():
    print("\n=== LAIKA Servo Control Interactive Mode ===")
    print("Available commands:")
    print("1. info <servo_id> - Get servo information")
    print("2. move <servo_id> <position> [time] - Move servo to position (0-1000)")
    print("3. ftest - Test front-side servo movement")
    print("4. btest - Test back-side servo movement")
    print("5. scan - Scan for available servos")
    print("6. set_temp <servo_id> <limit> - Set temperature limit")
    print("7. reset <servo_id> - Reset servo settings")
    print("8. assign <old_id> <new_id> - Change servo ID")
    print("9. help - Show this help message")
    print("10. quit - Exit interactive mode")
    print("=" * 45)

"""
Prints out the general servo motor's information
"""
def servo_info(id):
    print("Servo id: {}".format(id))
    print("Position: {}".format(ctrl.get_position(id)))
    print("Temperature: {}, limit: {}".format(ctrl.get_temperature(id), ctrl.get_max_temperature_limit(id)))
    print("Led error: {}".format(ctrl.get_led_errors(id)))

# Main function
if __name__ == "__main__":
    print_help()
    
    while True:
        try:
            user_input = input("\nEnter command: ").strip()
            
            if not user_input:
                continue
                
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == 'quit' or command == 'exit':
                print("Exiting program...")
                break
                
            elif command == 'help':
                print_help()
                
            elif command == 'info':
                if len(parts) < 2:
                    print("Usage: info <servo_id>")
                    continue
                try:
                    servo_id = int(parts[1])
                    servo_info(servo_id)
                except ValueError:
                    print("Error: Servo ID must be a number")
                except Exception as e:
                    print(f"Error getting servo info: {e}")
                    
            elif command == 'move':
                if len(parts) < 3:
                    print("Usage: move <servo_id> <position> [time_ms]")
                    continue
                try:
                    servo_id = int(parts[1])
                    position = int(parts[2])
                    time_ms = int(parts[3]) if len(parts) > 3 else 500
                    
                    if position < 0 or position > 1000:
                        print("Error: Position must be between 0 and 1000")
                        continue
                        
                    print(f"Moving servo {servo_id} to position {position} in {time_ms}ms...")
                    ctrl.move(servo_id, position, time_ms)
                    print("Move command sent successfully!")
                    
                except ValueError:
                    print("Error: All parameters must be numbers")
                except Exception as e:
                    print(f"Error moving servo: {e}")
                    
            elif command == 'ftest':
                try:
                    while True:
                        print(f"Moving servos 2 and 6...")
                        print("Moving to position 0...")
                        ctrl.move(2, 0)
                        ctrl.move(6, 0)
                        time.sleep(5)
                        print("Moving to position 1000...")
                        ctrl.move(2, 0)
                        ctrl.move(6, 0)
                        time.sleep(5)
                        #print("Moving to center position 500...")
                        #ctrl.move(2, 500, 2000)
                        #ctrl.move(6, 500, 2000)
                        #print("Test completed!")
                    
                    
                except ValueError:
                    print("Error: Servo ID must be a number")
                except Exception as e:
                    print(f"Error testing servo: {e}")
                    
            elif command == 'btest':
                try:
                    while True:
                        print(f"Moving servos 8 and 12...")
                        print("Moving to position 0...")
                        ctrl.move(8, 0)
                        ctrl.move(12, 0)
                        time.sleep(5)
                        print("Moving to position 1000...")
                        ctrl.move(8, 0)
                        ctrl.move(12, 0)
                        time.sleep(5)
                        #print("Moving to center position 500...")
                        #ctrl.move(2, 500, 2000)
                        #ctrl.move(6, 500, 2000)
                        #print("Test completed!")
                    
                except ValueError:
                    print("Error: Servo ID must be a number")
                except Exception as e:
                    print(f"Error testing servo: {e}")
                            
            elif command == 'scan':
                print("Scanning for servo motors...")
                found_servos = []
                for i in range(1, 255):
                    try:
                        ctrl.get_position(i, 0.03)
                        found_servos.append(i)
                        print(f"Found servo: {i}")
                    except:
                        pass
                        
                if found_servos:
                    print(f"\nTotal servos found: {len(found_servos)}")
                    print(f"Servo IDs: {found_servos}")
                else:
                    print("No servos found!")
                    
            elif command == 'set_temp':
                if len(parts) < 3:
                    print("Usage: set_temp <servo_id> <temperature_limit>")
                    continue
                try:
                    servo_id = int(parts[1])
                    temp_limit = int(parts[2])
                    print(f"Setting temperature limit for servo {servo_id} to {temp_limit}°C...")
                    ctrl.set_max_temperature_limit(servo_id, temp_limit)
                    print("Temperature limit set successfully!")
                    
                except ValueError:
                    print("Error: All parameters must be numbers")
                except Exception as e:
                    print(f"Error setting temperature limit: {e}")
                    
            elif command == 'reset':
                if len(parts) < 2:
                    print("Usage: reset <servo_id>")
                    continue
                try:
                    servo_id = int(parts[1])
                    print(f"Resetting servo {servo_id}...")
                    ctrl.set_position_offset(servo_id, 0)
                    time.sleep(0.1)
                    ctrl.save_position_offset(servo_id)
                    time.sleep(0.1)
                    ctrl.set_max_temperature_limit(servo_id, 85)
                    time.sleep(0.1)
                    ctrl.set_led_errors(servo_id, 7)
                    time.sleep(0.1)
                    ctrl.led_on(servo_id)
                    time.sleep(0.1)
                    ctrl.set_servo_id(servo_id, 1)
                    print("Servo reset completed!")
                    
                except ValueError:
                    print("Error: Servo ID must be a number")
                except Exception as e:
                    print(f"Error resetting servo: {e}")
                    
            elif command == 'assign':
                if len(parts) < 3:
                    print("Usage: assign <old_id> <new_id>")
                    continue
                try:
                    old_id = int(parts[1])
                    new_id = int(parts[2])
                    print(f"Changing servo ID from {old_id} to {new_id}...")
                    ctrl.set_servo_id(old_id, new_id)
                    print("Servo ID changed successfully!")
                    
                except ValueError:
                    print("Error: All parameters must be numbers")
                except Exception as e:
                    print(f"Error changing servo ID: {e}")
                    
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands or 'quit' to exit")
                
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
