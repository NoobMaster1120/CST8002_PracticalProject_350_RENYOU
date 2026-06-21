"""
CST8002 Programming Language Research Project
Practical Project Part 3

Professor: Update with your professor's name from Brightspace
Due Date: See Brightspace for due date
Author: REN YOU

References:
[1] GeeksforGeeks, "Types of Linked List," geeksforgeeks.org,
    [online]. Available: https://www.geeksforgeeks.org/dsa/types-of-linked-list/
    [Accessed: Jun. 20, 2026].
[2] Python Software Foundation, "8. Classes," Python Tutorial, docs.python.org,
    [online]. Available: https://docs.python.org/3/tutorial/classes.html
    [Accessed: Jun. 20, 2026].
"""

from typing import Generic, Iterator, TypeVar

from model.natural_gas_record import NaturalGasRecord

T = TypeVar("T")


class _ListNode(Generic[T]):
    """
    Self-referential node used as the building block of a singly linked list.

    Each node stores one data item and a reference to the next node.
    """

    def __init__(self, data: T, next_node: "_ListNode[T] | None" = None) -> None:
        """
        Initialize a list node.

        Args:
            data: Value stored in this node.
            next_node: Reference to the next node, or None at the tail.
        """
        self.data = data
        self.next = next_node


class SinglyLinkedList(Generic[T]):
    """
    Singly linked list collection implemented with basic programming techniques.

    This custom data structure replaces the Python list used in earlier project
    iterations for storing NaturalGasRecord objects in memory.
    """

    def __init__(self) -> None:
        """Initialize an empty singly linked list."""
        self._head: _ListNode[T] | None = None
        self._size = 0

    def __len__(self) -> int:
        """Return the number of nodes currently stored in the list."""
        return self._size

    def __iter__(self) -> Iterator[T]:
        """Iterate over each data item from head to tail."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def is_empty(self) -> bool:
        """Return True when the list contains no nodes."""
        return self._head is None

    def append(self, data: T) -> None:
        """
        Add a new node containing data at the tail of the list.

        Args:
            data: Item to store in the new tail node.
        """
        new_node = _ListNode(data)

        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self._size += 1

    def get(self, index: int) -> T:
        """
        Return the data stored at a zero-based index.

        Args:
            index: Position of the node to read.

        Returns:
            Data stored at the requested index.

        Raises:
            IndexError: If index is out of range.
        """
        node = self._get_node_at(index)
        return node.data

    def set(self, index: int, data: T) -> None:
        """
        Replace the data stored at a zero-based index.

        Args:
            index: Position of the node to update.
            data: New value to store in that node.

        Raises:
            IndexError: If index is out of range.
        """
        node = self._get_node_at(index)
        node.data = data

    def delete(self, index: int) -> T:
        """
        Remove and return the node data at a zero-based index.

        Args:
            index: Position of the node to remove.

        Returns:
            Data that was stored in the removed node.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("list index out of range")

        if index == 0:
            removed_node = self._head
            assert removed_node is not None
            self._head = removed_node.next
            self._size -= 1
            return removed_node.data

        previous = self._get_node_at(index - 1)
        removed_node = previous.next
        assert removed_node is not None
        previous.next = removed_node.next
        self._size -= 1
        return removed_node.data

    def clear(self) -> None:
        """Remove all nodes from the list."""
        self._head = None
        self._size = 0

    def replace_all(self, items: list[T]) -> None:
        """
        Replace the entire list contents with a new sequence of items.

        Args:
            items: Values to store in list order after clearing existing nodes.
        """
        self.clear()
        for item in items:
            self.append(item)

    def to_list(self) -> list[T]:
        """Return a Python list containing all items in linked-list order."""
        return list(self)

    def _get_node_at(self, index: int) -> _ListNode[T]:
        """
        Return the node at a zero-based index.

        Args:
            index: Position of the node to locate.

        Returns:
            The node stored at the requested index.

        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("list index out of range")

        current = self._head
        for _ in range(index):
            assert current is not None
            current = current.next

        assert current is not None
        return current


NaturalGasLinkedList = SinglyLinkedList[NaturalGasRecord]
