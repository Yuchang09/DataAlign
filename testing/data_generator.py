import numpy as np
import pandas as pd


def generate_test_data(
    filename="test_data.xlsx",
    duration=10,
    sampling_rate=1000
):
    # Time points
    time = np.arange(0, duration, 1 / sampling_rate)

    # --------------------------------------------------
    # 1. Neural activity
    # --------------------------------------------------

    # Baseline neural voltage
    neural_voltage = np.random.normal(
        loc=0,
        scale=1,
        size=len(time)
    )

    # Neural activity events
    #
    # Some overlap with tone/puff,
    # some do not.
    neural_events = [
        (0.5, 0.6),    # neural only

        (1.0, 1.2),    # overlaps tone

        (2.0, 2.2),    # overlaps puff

        (3.0, 3.3),    # overlaps tone partially

        (4.0, 4.1),    # neural only

        (5.0, 5.3),    # overlaps puff partially

        (7.0, 7.2),    # overlaps tone

        (9.0, 9.2),    # neural only
    ]

    for start, end in neural_events:
        mask = (time >= start) & (time < end)
        neural_voltage[mask] = 5

    # --------------------------------------------------
    # 2. Tone
    # --------------------------------------------------

    tone_voltage = np.zeros(len(time))

    tone_events = [
        (1.0, 1.2),    # exact overlap with neural

        (2.5, 2.7),    # tone only

        (3.2, 3.5),    # partially overlaps neural

        (6.0, 6.2),    # tone only

        (7.0, 7.2),    # exact overlap with neural

        (8.0, 8.2),    # tone only
    ]

    for start, end in tone_events:
        mask = (time >= start) & (time < end)
        tone_voltage[mask] = 5

    # --------------------------------------------------
    # 3. Puff
    # --------------------------------------------------

    puff_voltage = np.zeros(len(time))

    puff_events = [
        (2.0, 2.2),    # exact overlap with neural

        (3.8, 4.0),    # puff only

        (5.2, 5.5),    # partially overlaps neural

        (6.5, 6.7),    # puff only

        (8.5, 8.7),    # puff only

        (9.0, 9.2),    # overlaps neural
    ]

    for start, end in puff_events:
        mask = (time >= start) & (time < end)
        puff_voltage[mask] = 3

    # --------------------------------------------------
    # Put everything together
    # --------------------------------------------------

    df = pd.DataFrame({
        "Time": time,
        "NeuralVoltage": neural_voltage,
        "ToneVoltage": tone_voltage,
        "PuffVoltage": puff_voltage
    })

    # Save to Excel
    df.to_excel(filename, index=False)

    return df


df = generate_test_data()
