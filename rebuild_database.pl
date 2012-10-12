#!/usr/bin/perl
use DBI;
use strict;
use File::Copy;

# Note the missing -w. I'm lazy. And?

my $db = DBI->connect("dbi:SQLite:unswmate.db", "", "", {RaiseError => 1, AutoCommit => 0});


$db->do("DROP TABLE IF EXISTS users");
$db->do("DROP TABLE IF EXISTS mates");
$db->do("DROP TABLE IF EXISTS courses");
$db->do("DROP TABLE IF EXISTS images");

$db->do("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT, gender TEXT, degree TEXT, student_number INTEGER, about TEXT, profile_picture TEXT)");
$db->do("CREATE TABLE mates (id INTEGER PRIMARY KEY, user TEXT, mate TEXT)");
$db->do("CREATE TABLE courses (id INTEGER PRIMARY KEY, user TEXT, course TEXT)");
$db->do("CREATE TABLE images (id INTEGER PRIMARY KEY, user TEXT, image TEXT)");

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


# And we'll stick the images over here
my $image_dir = './data/images';
my $image_name_length = 12;
mkdir $image_dir or die "Couldn't make directory $image_dir";

foreach my $user (@all_users) {
    print "Migrating images for $user\n";
    my @images = glob($user.'/*.jpg');
    $user =~ s/\.\/users\///;
    foreach my $image (@images) {
        my $new_name = random_alphanum().'.jpg'; 
        while (-e $image_dir.'/'.$new_name) {
            $new_name = random_alphanum().'.jpg'; 
        }
        print $new_name."\n";
        my $image_full = $image_dir.'/'.$new_name;
        # We have a unique name, yay
        copy($image, $image_full);
        if ($image =~ /profile\.jpg/) {
            $db->do("UPDATE users SET profile_picture='".$image_full."' WHERE username='".$user."'")
        }
        $db->do("INSERT INTO images VALUES (NULL, '".$user."', '".$image_full."')")
   }
    $db->do("COMMIT");
}

sub random_alphanum {
    my $string = '';
    foreach (1 .. $image_name_length) {
       my $random = int(rand(62));
       if ($random <= 25) {
           $string .= chr(ord('a')+$random);
       } elsif ($random >= 52) {
           $string .= chr(ord('0')+($random-52));
       } elsif ($random >= 26 and $random le 51) {
           $string .= chr(ord('A')+($random-26));
       }
   }
   return $string;
}
