<?php
$object = new class implements ArrayAccess {
    public function offsetGet($offset)
    {
        return [1, 2];
    }
    public function offsetExists($offset)
    {
        return true;
    }
    public function offsetUnset($offset) {}
    public function offsetSet($offset, $value) {}
};
var_dump(max(...$object[0]));
?>