import argparse

from cust_eval import model, output
from cust_eval.data_processing import transform_data


def main():
    parser = argparse.ArgumentParser(description='Customer Evaluation CLI Tool')
    parser.add_argument('command', choices=['count', 'spend'])
    parser.add_argument('-n', type=int, required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    # Load data
    data = transform_data(args.input)

    # Predict
    data = model.predict(data, args.command, 1)

    data = output.modelOut(data, args.n)

    # Save to output CSV
    data.to_csv(args.output, index=False)


if __name__ == '__main__':
    main()
