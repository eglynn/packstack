
class {"mysql::server": 
    config_hash => {bind_address => "0.0.0.0"}
} 

class {"keystone::db::mysql": 
    allowed_hosts => "%%",
} 

class {"glance::db::mysql":
    allowed_hosts => "%%",
    password      => "glance_default_password",
}
   
class {"nova::db::mysql":
    allowed_hosts => "%%",
    password      => "nova_password",
}

firewall { '001 mysql incomming':
    proto    => 'tcp',
    dport    => ['3306'],
    action   => 'accept',
}