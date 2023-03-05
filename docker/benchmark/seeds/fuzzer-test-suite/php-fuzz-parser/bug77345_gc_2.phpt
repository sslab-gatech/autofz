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

function xxx() {
    $firstNode = new Node();
    $firstNode->previous = $firstNode;
    $firstNode->next = $firstNode;

    $circularDoublyLinkedList = $firstNode;

    for ($i = 0; $i < 300000; $i++) {
        $currentNode = $circularDoublyLinkedList;
        $nextNode = $circularDoublyLinkedList->next;

        $newNode = new Node();

        $newNode->previous = $currentNode;
        $currentNode->next = $newNode;
        $newNode->next = $nextNode;
        $nextNode->previous = $newNode;

        $circularDoublyLinkedList = $nextNode;
    }
}

xxx();
gc_collect_cycles();

var_dump('end');