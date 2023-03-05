<?php

class A
{
    var $_stdObject;
    function __construct()
    {
        $this->_stdObject = new stdClass;
    }
    function &__get($property)
    {
        if (isset($this->_stdObject->{$property})) {
            $retval =& $this->_stdObject->{$property};
            return $retval;
        } else {
            return NULL;
        }
    }
    function &__set($property, $value)
    {
        return $this->_stdObject->{$property} = $value;
    }
    function __isset($property_name)
    {
        return isset($this->_stdObject->{$property_name});
    }
}

class B extends A
{
    function &__get($property)
    {
        if (isset($this->settings) && isset($this->settings[$property])) {
            $retval =& $this->settings[$property];
            return $retval;
        } else {
            return parent::__get($property);
        }
    }
}

$b = new B();
$b->settings = [ "foo" => "bar", "name" => "abc" ];
var_dump($b->name);
var_dump($b->settings);
?>