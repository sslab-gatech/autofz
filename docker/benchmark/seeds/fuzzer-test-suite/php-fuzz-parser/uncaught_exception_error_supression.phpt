<?php

function abc() {
    throw new Error('Example Exception');
}

@abc();

?>