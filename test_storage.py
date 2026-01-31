from storage import DataStore
import os

def test_storage():
    filename = "test_data.json"
    if os.path.exists(filename):
        os.remove(filename)

    store = DataStore(filename)
    print("Updating usage for 'TestApp'...")
    store.update_usage("TestApp", 5)
    store.update_usage("TestApp", 5)
    
    data = store.get_usage()
    print(f"Usage data: {data}")
    
    if data.get("TestApp") == 10:
        print("SUCCESS: Data persisted correctly.")
    else:
        print("FAILURE: Data mismatch.")

    # Clean up
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    test_storage()
