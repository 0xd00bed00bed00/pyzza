from typing import Union
from datetime import datetime

class RunContanerKwargs:
    image = None
    command = None
    auto_remove = None
    blkio_weight_device = None
    blkio_weight = None
    cap_add = None
    cap_drop = None
    cgroup_parent = None
    cgroupns = None
    cpu_count = None
    cpu_quota = None
    cpu_rt_period = None
    cpu_rt_runtime = None
    cpu_shares = None
    cpuset_cpus = None
    cpuset_mems = None
    detach = None
    device_cgroup_rules = None
    device_read_bps = None
    device_read_iops = None
    device_write_bps = None
    device_write_iops = None
    devices = None
    device_requests = None
    dns = None
    dns_opt = None
    domainname = None
    entrypoint = None
    environment = None
    extra_hosts = None
    group_add = None
    healthcheck = None
    hostname = None
    init = None
    init_path = None
    ipc_mode = None
    isolation = None
    kernel_memory = None
    labels = None
    links = None
    log_config = None
    lxc_conf = None
    mac_address = None
    mem_limit = None
    mem_reservation = None
    mem_swappiness = None
    memswap_limit = None
    mounts = None
    name = None
    nano_cpus = None
    network = None
    network_disabled = None
    network_mode = None
    network_driver_opt = None
    oom_kill_disable = None
    oom_score_adj = None
    pid_mode = None
    pids_limit = None
    platform = None
    ports = None
    privileged = None
    publish_all_ports = None
    read_only = None
    remove = None
    restart_policy = None
    runtime = None
    security_opt = None
    shm_size = None
    stdin_open = None
    stdout = None
    stderr = None
    stop_signal = None
    storage_opt = None
    stream = None
    sysctls = None
    tmpfs = None
    tty = None
    ulimits = None
    use_config_proxy = None
    user = None
    userns_mode = None
    uts_mode = None
    version = None
    volume_driver = None
    volumes = None
    volumes_from = None
    working_dir = None
    def __init__(self,
        image = None,
        command = None,
        auto_remove = None,
        blkio_weight_device = None,
        blkio_weight = None,
        cap_add = None,
        cap_drop = None,
        cgroup_parent = None,
        cgroupns = None,
        cpu_count = None,
        cpu_quota = None,
        cpu_rt_period = None,
        cpu_rt_runtime = None,
        cpu_shares = None,
        cpuset_cpus = None,
        cpuset_mems = None,
        detach = None,
        device_cgroup_rules = None,
        device_read_bps = None,
        device_read_iops = None,
        device_write_bps = None,
        device_write_iops = None,
        devices = None,
        device_requests = None,
        dns = None,
        dns_opt = None,
        domainname = None,
        entrypoint = None,
        environment = None,
        extra_hosts = None,
        group_add = None,
        healthcheck = None,
        hostname = None,
        init = None,
        init_path = None,
        ipc_mode = None,
        isolation = None,
        kernel_memory = None,
        labels = None,
        links = None,
        log_config = None,
        lxc_conf = None,
        mac_address = None,
        mem_limit = None,
        mem_reservation = None,
        mem_swappiness = None,
        memswap_limit = None,
        mounts = None,
        name = None,
        nano_cpus = None,
        network = None,
        network_disabled = None,
        network_mode = None,
        network_driver_opt = None,
        oom_kill_disable = None,
        oom_score_adj = None,
        pid_mode = None,
        pids_limit = None,
        platform = None,
        ports = None,
        privileged = None,
        publish_all_ports = None,
        read_only = None,
        remove = False,
        restart_policy = None,
        runtime = None,
        security_opt = None,
        shm_size = None,
        stdin_open = None,
        stdout = True,
        stderr = False,
        stop_signal = None,
        storage_opt = None,
        stream = False,
        sysctls = None,
        tmpfs = None,
        tty = None,
        ulimits = None,
        use_config_proxy = None,
        user = None,
        userns_mode = None,
        uts_mode = None,
        version = None,
        volume_driver = None,
        volumes = None,
        volumes_from = None,
        working_dir = None,
    ):
        self.image = image
        self.command = command
        self.auto_remove = auto_remove
        self.blkio_weight_device = blkio_weight_device
        self.blkio_weight = blkio_weight
        self.cap_add = cap_add
        self.cap_drop = cap_drop
        self.cgroup_parent = cgroup_parent
        self.cgroupns = cgroupns
        self.cpu_count = cpu_count
        self.cpu_quota = cpu_quota
        self.cpu_rt_period = cpu_rt_period
        self.cpu_rt_runtime = cpu_rt_runtime
        self.cpu_shares = cpu_shares
        self.cpuset_cpus = cpuset_cpus
        self.cpuset_mems = cpuset_mems
        self.detach = detach
        self.device_cgroup_rules = device_cgroup_rules
        self.device_read_bps = device_read_bps
        self.device_read_iops = device_read_iops
        self.device_write_bps = device_write_bps
        self.device_write_iops = device_write_iops
        self.devices = devices
        self.device_requests = device_requests
        self.dns = dns
        self.dns_opt = dns_opt
        self.domainname = domainname
        self.entrypoint = entrypoint
        self.environment = environment
        self.extra_hosts = extra_hosts
        self.group_add = group_add
        self.healthcheck = healthcheck
        self.hostname = hostname
        self.init = init
        self.init_path = init_path
        self.ipc_mode = ipc_mode
        self.isolation = isolation
        self.kernel_memory = kernel_memory
        self.labels = labels
        self.links = links
        self.log_config = log_config
        self.lxc_conf = lxc_conf
        self.mac_address = mac_address
        self.mem_limit = mem_limit
        self.mem_reservation = mem_reservation
        self.mem_swappiness = mem_swappiness
        self.memswap_limit = memswap_limit
        self.mounts = mounts
        self.name = name
        self.nano_cpus = nano_cpus
        self.network = network
        self.network_disabled = network_disabled
        self.network_mode = network_mode
        self.network_driver_opt = network_driver_opt
        self.oom_kill_disable = oom_kill_disable
        self.oom_score_adj = oom_score_adj
        self.pid_mode = pid_mode
        self.pids_limit = pids_limit
        self.platform = platform
        self.ports = ports
        self.privileged = privileged
        self.publish_all_ports = publish_all_ports
        self.read_only = read_only
        self.remove = remove
        self.restart_policy = restart_policy
        self.runtime = runtime
        self.security_opt = security_opt
        self.shm_size = shm_size
        self.stdin_open = stdin_open
        self.stdout = stdout
        self.stderr = stderr
        self.stop_signal = stop_signal
        self.storage_opt = storage_opt
        self.stream = stream
        self.sysctls = sysctls
        self.tmpfs = tmpfs
        self.tty = tty
        self.ulimits = ulimits
        self.use_config_proxy = use_config_proxy
        self.user = user
        self.userns_mode = userns_mode
        self.uts_mode = uts_mode
        self.version = version
        self.volume_driver = volume_driver
        self.volumes = volumes
        self.volumes_from = volumes_from
        self.working_dir = working_dir

class CreateContanerKwargs:
    image = None
    command = None
    auto_remove = None
    blkio_weight_device = None
    blkio_weight = None
    cap_add = None
    cap_drop = None
    cgroup_parent = None
    cgroupns = None
    cpu_count = None
    cpu_quota = None
    cpu_rt_period = None
    cpu_rt_runtime = None
    cpu_shares = None
    cpuset_cpus = None
    cpuset_mems = None
    detach = None
    device_cgroup_rules = None
    device_read_bps = None
    device_read_iops = None
    device_write_bps = None
    device_write_iops = None
    devices = None
    device_requests = None
    dns = None
    dns_opt = None
    domainname = None
    entrypoint = None
    environment = None
    extra_hosts = None
    group_add = None
    healthcheck = None
    hostname = None
    init = None
    init_path = None
    ipc_mode = None
    isolation = None
    kernel_memory = None
    labels = None
    links = None
    log_config = None
    lxc_conf = None
    mac_address = None
    mem_limit = None
    mem_reservation = None
    mem_swappiness = None
    memswap_limit = None
    mounts = None
    name = None
    nano_cpus = None
    network = None
    network_disabled = None
    network_mode = None
    network_driver_opt = None
    oom_kill_disable = None
    oom_score_adj = None
    pid_mode = None
    pids_limit = None
    platform = None
    ports = None
    privileged = None
    publish_all_ports = None
    read_only = None
    restart_policy = None
    runtime = None
    security_opt = None
    shm_size = None
    stdin_open = None
    stop_signal = None
    storage_opt = None
    #stream = None
    sysctls = None
    tmpfs = None
    tty = None
    ulimits = None
    use_config_proxy = None
    user = None
    userns_mode = None
    uts_mode = None
    version = None
    volume_driver = None
    volumes = None
    volumes_from = None
    working_dir = None
    def __init__(self,
        image = None,
        command = None,
        auto_remove = None,
        blkio_weight_device = None,
        blkio_weight = None,
        cap_add = None,
        cap_drop = None,
        cgroup_parent = None,
        cgroupns = None,
        cpu_count = None,
        cpu_quota = None,
        cpu_rt_period = None,
        cpu_rt_runtime = None,
        cpu_shares = None,
        cpuset_cpus = None,
        cpuset_mems = None,
        detach = None,
        device_cgroup_rules = None,
        device_read_bps = None,
        device_read_iops = None,
        device_write_bps = None,
        device_write_iops = None,
        devices = None,
        device_requests = None,
        dns = None,
        dns_opt = None,
        domainname = None,
        entrypoint = None,
        environment = None,
        extra_hosts = None,
        group_add = None,
        healthcheck = None,
        hostname = None,
        init = None,
        init_path = None,
        ipc_mode = None,
        isolation = None,
        kernel_memory = None,
        labels = None,
        links = None,
        log_config = None,
        lxc_conf = None,
        mac_address = None,
        mem_limit = None,
        mem_reservation = None,
        mem_swappiness = None,
        memswap_limit = None,
        mounts = None,
        name = None,
        nano_cpus = None,
        network = None,
        network_disabled = None,
        network_mode = None,
        network_driver_opt = None,
        oom_kill_disable = None,
        oom_score_adj = None,
        pid_mode = None,
        pids_limit = None,
        platform = None,
        ports = None,
        privileged = None,
        publish_all_ports = None,
        read_only = None,
        restart_policy = None,
        runtime = None,
        security_opt = None,
        shm_size = None,
        stdin_open = None,
        stop_signal = None,
        storage_opt = None,
        #stream = False,
        sysctls = None,
        tmpfs = None,
        tty = None,
        ulimits = None,
        use_config_proxy = None,
        user = None,
        userns_mode = None,
        uts_mode = None,
        version = None,
        volume_driver = None,
        volumes = None,
        volumes_from = None,
        working_dir = None,
    ):
        self.image = image
        self.command = command
        self.auto_remove = auto_remove
        self.blkio_weight_device = blkio_weight_device
        self.blkio_weight = blkio_weight
        self.cap_add = cap_add
        self.cap_drop = cap_drop
        self.cgroup_parent = cgroup_parent
        self.cgroupns = cgroupns
        self.cpu_count = cpu_count
        self.cpu_quota = cpu_quota
        self.cpu_rt_period = cpu_rt_period
        self.cpu_rt_runtime = cpu_rt_runtime
        self.cpu_shares = cpu_shares
        self.cpuset_cpus = cpuset_cpus
        self.cpuset_mems = cpuset_mems
        self.detach = detach
        self.device_cgroup_rules = device_cgroup_rules
        self.device_read_bps = device_read_bps
        self.device_read_iops = device_read_iops
        self.device_write_bps = device_write_bps
        self.device_write_iops = device_write_iops
        self.devices = devices
        self.device_requests = device_requests
        self.dns = dns
        self.dns_opt = dns_opt
        self.domainname = domainname
        self.entrypoint = entrypoint
        self.environment = environment
        self.extra_hosts = extra_hosts
        self.group_add = group_add
        self.healthcheck = healthcheck
        self.hostname = hostname
        self.init = init
        self.init_path = init_path
        self.ipc_mode = ipc_mode
        self.isolation = isolation
        self.kernel_memory = kernel_memory
        self.labels = labels
        self.links = links
        self.log_config = log_config
        self.lxc_conf = lxc_conf
        self.mac_address = mac_address
        self.mem_limit = mem_limit
        self.mem_reservation = mem_reservation
        self.mem_swappiness = mem_swappiness
        self.memswap_limit = memswap_limit
        self.mounts = mounts
        self.name = name
        self.nano_cpus = nano_cpus
        self.network = network
        self.network_disabled = network_disabled
        self.network_mode = network_mode
        self.network_driver_opt = network_driver_opt
        self.oom_kill_disable = oom_kill_disable
        self.oom_score_adj = oom_score_adj
        self.pid_mode = pid_mode
        self.pids_limit = pids_limit
        self.platform = platform
        self.ports = ports
        self.privileged = privileged
        self.publish_all_ports = publish_all_ports
        self.read_only = read_only
        self.restart_policy = restart_policy
        self.runtime = runtime
        self.security_opt = security_opt
        self.shm_size = shm_size
        self.stdin_open = stdin_open
        self.stop_signal = stop_signal
        self.storage_opt = storage_opt
        #self.stream = stream
        self.sysctls = sysctls
        self.tmpfs = tmpfs
        self.tty = tty
        self.ulimits = ulimits
        self.use_config_proxy = use_config_proxy
        self.user = user
        self.userns_mode = userns_mode
        self.uts_mode = uts_mode
        self.version = version
        self.volume_driver = volume_driver
        self.volumes = volumes
        self.volumes_from = volumes_from
        self.working_dir = working_dir

class BuildImageKwargs:
    path = None
    fileobj = None
    tag = None
    quiet = None
    nocache = None
    rm = None
    timeout = None
    custom_context = None
    encoding = None
    pull = None
    forcerm = None
    dockerfile = None
    buildargs = None
    container_limits = None
    shmsize = None
    labels = None
    cache_from = None
    target = None
    network_mode = None
    squash = None
    extra_hosts = None
    platform = None
    isolation = None
    use_config_proxy = None
    def __init__(self,
        path = None,
        fileobj = None,
        tag = None,
        quiet = None,
        nocache = None,
        rm = True,
        timeout = None,
        custom_context = None,
        encoding = None,
        pull = None,
        forcerm = None,
        dockerfile = None,
        buildargs = None,
        container_limits = None,
        shmsize = None,
        labels = None,
        cache_from = None,
        target = None,
        network_mode = None,
        squash = None,
        extra_hosts = None,
        platform = None,
        isolation = None,
        use_config_proxy = None,
    ):
        self.path = path
        self.fileobj = fileobj
        self.tag = tag
        self.quiet = quiet
        self.nocache = nocache
        self.rm = rm
        self.timeout = timeout
        self.custom_context = custom_context
        self.encoding = encoding
        self.pull = pull
        self.forcerm = forcerm
        self.dockerfile = dockerfile
        self.buildargs = buildargs
        self.container_limits = container_limits
        self.shmsize = shmsize
        self.labels = labels
        self.cache_from = cache_from
        self.target = target
        self.network_mode = network_mode
        self.squash = squash
        self.extra_hosts = extra_hosts
        self.platform = platform
        self.isolation = isolation
        self.use_config_proxy = use_config_proxy

class ContainerLogsKwargs:
    stdout: bool = None
    stderr: bool = None
    stream = None
    timestamps = None
    tail = None
    since = None
    follow = None
    until = None
    def __init__(self,
        stdout=True,
        stderr=True,
        stream=False,
        timestamps=False,
        tail='all',
        since=None,
        follow=False,
        until=None,
    ):
        self.stdout=stdout
        self.stderr=stderr
        self.stream=stream
        self.timestamps=timestamps
        self.tail=tail
        self.since=since
        self.follow=follow
        self.until=until
