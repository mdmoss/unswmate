#!/usr/bin/perl
use DBI;
use strict;

# Note the missing -w. I'm lazy. And?

my $db = DBI->connect("dbi:SQLite:unswmate.db", "", "", {RaiseError => 1, AutoCommit => 0});

$db->do("DROP TABLE IF EXISTS users");
$db->do("DROP TABLE IF EXISTS mates");
$db->do("DROP TABLE IF EXISTS courses");

$db->do("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT, gender TEXT, degree TEXT, student_number INTEGER, about TEXT)");
$db->do("CREATE TABLE mates (id INTEGER PRIMARY KEY, user TEXT, mate TEXT)");
$db->do("CREATE TABLE courses (id INTEGER PRIMARY KEY, user TEXT, course TEXT)");

# Database created. Lets get populatin'
    
my @all_users = <./users/*>;
foreach my $user (@all_users) {
    my %data = ();
    my $active_var = '';
    my @courses = ();
    my @mates = ();
    
    open (F, "$user/details.txt");
    while (my $line = <F>) {
        if ($line =~ /(\w+):/) {
            $active_var = $1;
        } elsif ($line =~ /^\s*(.*?)\s*$/){
        
            my $value = $1;
        
            if ($active_var =~ /mates/) {
                push (@mates, $value);
            } elsif ($active_var =~ /courses/) {
                push (@courses, $value);
            } else {
                $data{$active_var} = $value;
            }
        }
    }
    
    printf ("Writing db: $data{'username'}\n");
    
    $db->do("INSERT INTO users VALUES (NULL, '".$data{'username'}."', '".$data{'password'}."', '".$data{'name'}."', '".$data{'email'}."', '".$data{'gender'}."', '".$data{'degree'}."', '".$data{'student_number'}."', '".$data{'about'}."')");
    
    for my $mate (@mates) {
        $db->do("INSERT INTO mates VALUES (NULL, '".$data{'username'}."', '".$mate."')");
    }
    
    for my $course (@courses) {
        $db->do("INSERT INTO courses VALUES (NULL, '".$data{'username'}."', '".$course."')");
    }
    
    $db->do("COMMIT");
}