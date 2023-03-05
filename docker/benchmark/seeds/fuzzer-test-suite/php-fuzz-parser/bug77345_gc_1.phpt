<?php

class Node
{
    /** @var Node */
    public $previous;
    /** @var Node */
    public $next;
}

var_dump(gc_enabled());
var_dump('start');

$firstNode = new Node();
$firstNode->previous = $firstNode;
$firstNode->next = $firstNode;

$circularDoublyLinkedList = $firstNode;

for ($i = 0; $i < 200000; $i++) {
    $currentNode = $circularDoublyLinkedList;
    $nextNode = $circularDoublyLinkedList->next;

    $newNode = new Node();

    $newNode->previous = $currentNode;
    $currentNode->next = $newNode;
    $newNode->next = $nextNode;
    $nextNode->previous = $newNode;

    $circularDoublyLinkedList = $nextNode;
}
var_dump('end');