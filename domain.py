import os

HOSTS_FILE = '/etc/hosts'
BEGIN_TAG = '#custom-my-ap-begin'
END_TAG = '#custom-my-ap-end'

def read_hosts_file():
    """Read the content of /etc/hosts and return as a list of lines."""
    with open(HOSTS_FILE, 'r') as f:
        return f.readlines()

def write_hosts_file(lines):
    """Write back the content to /etc/hosts."""
    with open(HOSTS_FILE, 'w') as f:
        f.writelines(lines)

def get_custom_block_indices(lines):
    """Find the indices of the custom block in the hosts file."""
    begin_index = None
    end_index = None
    for i, line in enumerate(lines):
        if BEGIN_TAG in line:
            begin_index = i
        if END_TAG in line:
            end_index = i
            break
    return begin_index, end_index

def update_or_add_custom_block(lines, new_domains):
    """Add or update the custom block in the hosts file."""
    begin_index, end_index = get_custom_block_indices(lines)
    
    # If the custom block is found, replace its contents
    if begin_index is not None and end_index is not None:
        # Keep everything before the begin tag, add new domains, and everything after the end tag
        updated_lines = lines[:begin_index + 1]
        updated_lines.extend([f"{domain}\n" for domain in new_domains])
        updated_lines.extend(lines[end_index:])
        return updated_lines
    else:
        # If the block is not found, append it at the end
        lines.append(f"\n{BEGIN_TAG}\n")
        lines.extend([f"{domain}\n" for domain in new_domains])
        lines.append(f"{END_TAG}\n")
        return lines

def manage_custom_domains():
    # Step 1: Read the hosts file
    lines = read_hosts_file()
    
    # Step 2: Display current custom block content (if any)
    begin_index, end_index = get_custom_block_indices(lines)
    if begin_index is not None and end_index is not None:
        print("Current custom domains:")
        custom_block = lines[begin_index + 1:end_index]
        print("".join(custom_block))
    else:
        print("No custom block found.")
    
    # Step 3: Ask user to add new custom domains
    print("Enter the new custom domains (leave empty to skip):")
    new_domains = []
    while True:
        domain = input("Enter domain (format: IP domain): ").strip()
        if not domain:
            break
        new_domains.append(domain)
    
    # Step 4: Update the hosts file
    if new_domains:
        lines = update_or_add_custom_block(lines, new_domains)
        write_hosts_file(lines)
        print("Custom block updated successfully!")
    else:
        print("No new domains added.")

if __name__ == '__main__':
    if os.geteuid() != 0:
        print("Please run this script as root (or with sudo) to modify /etc/hosts.")
    else:
        manage_custom_domains()
