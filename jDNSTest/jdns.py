import dns.resolver
import time
import datetime
import json
import matplotlib.pyplot as plt
import pandas as pd

# List of popular websites to test
websites = [
    "google.com",
    "facebook.com",
    "youtube.com",
    "amazon.com",
    "wikipedia.org",
    "twitter.com",
    "instagram.com",
    "linkedin.com",
    "netflix.com",
    "yahoo.com"
]

# List of DNS servers to test
dns_servers = [
    "1.1.1.1",
    "75.75.75.75",
    "75.75.76.76"
]

# Number of times to test each website
num_tests = 5


# Function to perform DNS lookup and measure the time taken
def dns_lookup_time(website, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    start_time = time.time()
    try:
        resolver.resolve(website, 'A')
        end_time = time.time()
        lookup_time = (end_time - start_time) * 1000  # convert to milliseconds
        return lookup_time
    except dns.exception.DNSException as e:
        print(f"Error resolving {website} using {dns_server}: {e}")
        return None


# Function to perform the tests and collect data
def perform_tests(websites, dns_servers, num_tests):
    test_results = []
    for website in websites:
        for dns_server in dns_servers:
            for test_num in range(num_tests):
                lookup_time = dns_lookup_time(website, dns_server)
                test_result = {
                    "website": website,
                    "dns_server": dns_server,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "lookup_time_ms": lookup_time,
                    "test_number": test_num + 1
                }
                test_results.append(test_result)
    return test_results


# Function to visualize the results
def visualize_results(test_results):
    # Create a DataFrame from the test results
    df = pd.DataFrame(test_results)

    # Filter out rows with None lookup times
    df = df[df['lookup_time_ms'].notna()]

    # Create a line plot for each website showing the lookup times for each DNS server
    fig, ax = plt.subplots(figsize=(15, 10))
    for dns_server in dns_servers:
        server_data = df[df['dns_server'] == dns_server]
        for website in websites:
            website_data = server_data[server_data['website'] == website]
            ax.plot(website_data['test_number'], website_data['lookup_time_ms'], marker='o',
                    label=f"{website} ({dns_server})")

    ax.set_title('DNS Lookup Time Comparison')
    ax.set_xlabel('Test Number')
    ax.set_ylabel('Lookup Time (ms)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1), title="Website (DNS Server)")
    plt.tight_layout()
    plt.show()

    # Calculate and print summary statistics
    summary = df.groupby(['website', 'dns_server'])['lookup_time_ms'].describe()
    print(summary)


# Perform the tests and collect the data
test_results = perform_tests(websites, dns_servers, num_tests)

# Print the results
print(json.dumps(test_results, indent=4))

# Optionally, save the results to a file
with open("dns_test_results.json", "w") as f:
    json.dump(test_results, f, indent=4)

# Visualize the results
visualize_results(test_results)
