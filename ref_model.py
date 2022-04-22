from hashlib import sha256

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def main():
    print("Ref Model working fine")    
    
if __name__ == "__main__":
    main()