<?php
class SampleFilter extends php_user_filter { }
stream_filter_register('sample.filter', SampleFilter::class);
include 'php://filter/read=sample.filter/resource='. __FILE__;
?>