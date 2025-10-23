import csv

def ghi_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)

    print(f"✅ Đã ghi toàn bộ dữ liệu từ '{input_file}' sang '{output_file}'.")

if __name__ == "__main__":
    ghi_csv('stroke_copy.csv', 'git_csv.csv')
