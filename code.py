import logging
import os

# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    filename="library_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -------------------- TASK 1: BOOK CLASS --------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_line(self):
        """Convert book to a single text line for saving."""
        return f"{self.title}|{self.author}|{self.isbn}|{self.status}"

    @staticmethod
    def from_line(line):
        """Convert text line back into a Book object."""
        parts = line.strip().split("|")
        if len(parts) == 4:
            return Book(parts[0], parts[1], parts[2], parts[3])
        return None

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


# -------------------- TASK 2: INVENTORY MANAGER --------------------
class LibraryInventory:
    def __init__(self, filename="books.txt"):
        self.filename = filename
        self.books = []
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")
        print("Book added successfully.\n")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books available.\n")
            return
        for b in self.books:
            print(b)

    # -------------------- TASK 3: TEXT FILE PERSISTENCE --------------------
    def save_books(self):
        try:
            with open(self.filename, "w") as f:
                for b in self.books:
                    f.write(b.to_line() + "\n")

            logging.info("Books saved to text file.")
        except Exception as e:
            logging.error(f"Error saving books: {str(e)}")

    def load_books(self):
        try:
            if not os.path.exists(self.filename):
                return

            with open(self.filename, "r") as f:
                for line in f:
                    book = Book.from_line(line)
                    if book:
                        self.books.append(book)

            logging.info("Books loaded from text file.")
        except Exception as e:
            logging.error(f"Error loading file: {str(e)}")
            print("Warning: Could not load book data. File may be corrupted.\n")


# -------------------- TASK 4: MENU-DRIVEN CLI --------------------
def menu():
    inventory = LibraryInventory()

    while True:
        print("\n========== Library Menu ==========")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")
        print("==================================")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Enter numbers only.\n")
            continue

        # -------------------- ADD BOOK --------------------
        if choice == 1:
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")

            book = Book(title, author, isbn)
            inventory.add_book(book)
            inventory.save_books()

        # -------------------- ISSUE BOOK --------------------
        elif choice == 2:
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)

            if book:
                if book.issue():
                    print("Book issued successfully.")
                    logging.info(f"Issued: {book.title}")
                else:
                    print("Book already issued.")
            else:
                print("Book not found.")

            inventory.save_books()

        # -------------------- RETURN BOOK --------------------
        elif choice == 3:
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)

            if book:
                if book.return_book():
                    print("Book returned successfully.")
                    logging.info(f"Returned: {book.title}")
                else:
                    print("Book was not issued.")
            else:
                print("Book not found.")

            inventory.save_books()

        # -------------------- VIEW ALL --------------------
        elif choice == 4:
            print("\n--- All Books ---")
            inventory.display_all()

        # -------------------- SEARCH BOOK --------------------
        elif choice == 5:
            keyword = input("Enter title or ISBN: ")

            book = inventory.search_by_isbn(keyword)
            if book:
                print("\nBook Found:")
                print(book)
                continue

            results = inventory.search_by_title(keyword)
            if results:
                print("\nSearch Results:")
                for b in results:
                    print(b)
            else:
                print("No books found.")

        # -------------------- EXIT --------------------
        elif choice == 6:
            print("Saving and exiting... Goodbye!")
            inventory.save_books()
            break

        else:
            print("Invalid choice. Try again.")


# -------------------- RUN THE PROGRAM --------------------
if __name__ == "__main__":
    menu()