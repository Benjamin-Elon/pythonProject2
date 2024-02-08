import plotly.graph_objects as go
import math


def plot_solar_panel_output_interactive(outputs):
    """
    Plots the solar panel output at different angles using Plotly for an interactive graph.

    Parameters:
    outputs (dict): A dictionary with angles as keys and power output as values.
    """
    angles = list(outputs.keys())
    power_outputs = list(outputs.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=angles, y=power_outputs, mode='lines+markers', name='Power Output'))

    fig.update_layout(title='Solar Panel Power Output vs. Angle',
                      xaxis_title='Angle (degrees)',
                      yaxis_title='Power Output (Watts)',
                      template="plotly_dark")

    fig.show()


def solar_panel_output_at_angles(max_output):
    """
    Calculate the solar panel's power output at different angles.

    Parameters:
    max_output (float): Maximum power output of the solar panel in Watts.
    efficiency (float): Efficiency of the solar panel as a decimal.

    Returns:
    dict: A dictionary with angles (0-90 degrees) as keys and power output as values.
    """
    angle_outputs = {}
    for angle in range(91):  # Iterate through angles from 0 to 90 degrees
        # Calculate the output at this angle considering the cosine of the angle
        output_at_angle = max_output * math.cos(math.radians(angle))
        angle_outputs[angle] = output_at_angle
    return angle_outputs


def calculate_solar_panel_size(motor_power, motor_efficiency, panel_efficiency, solar_irradiance):
    """
    Calculate the required solar panel size based on motor power and efficiencies.

    Parameters:
    motor_power (float): Power requirement of the motor in Watts.
    motor_efficiency (float): Efficiency of the motor as a decimal.
    panel_efficiency (float): Efficiency of the solar panel as a decimal.
    solar_irradiance (float): Solar irradiance in Watts per square meter.

    Returns:
    float: Required solar panel area in square meters.
    """
    # Adjust motor power requirement based on its efficiency
    adjusted_motor_power = motor_power / motor_efficiency

    # Calculate the required solar panel size
    required_panel_power = adjusted_motor_power
    solar_panel_area = required_panel_power / (solar_irradiance * panel_efficiency)
    solar_power_output = solar_panel_area * solar_irradiance * panel_efficiency
    print("solar panel output = ", solar_power_output)
    return solar_panel_area, required_panel_power


def power_output_at_angles(motor_min_power, panel_max_output, panel_efficiency):
    """
    Determine the maximum angle from a light source before the motor won't turn.

    Parameters:
    motor_min_power (float): Minimum power required by the motor in Watts.
    panel_max_output (float): Maximum power output of the solar panel in Watts.
    panel_efficiency (float): Efficiency of the solar panel as a decimal.

    Returns:
    int: Maximum angle in degrees before the motor won't turn.
    """
    for angle in range(91):
        # Calculate the solar panel's output at this angle
        output_at_angle = panel_max_output * panel_efficiency * math.cos(math.radians(angle))
        # Check if the output is less than the minimum required power for the motor
        if output_at_angle < motor_min_power:
            # Return the last angle where the motor could operate
            return angle - 1
    # Return 90 if the motor can operate at all angles
    return 90


def main():
    """
    Main function to run the solar panel and motor calculator.
    """
    print("Solar Panel and Motor Calculator")
    motor_power = float(input("Enter motor power in Watts: "))
    motor_efficiency = float(input("Enter motor efficiency (as a decimal): "))
    motor_load_percentage = float(input("Enter motor load as a percentage of rated load: "))
    # Get user inputs for motor and solar panel specifications
    panel_efficiency = float(input("Enter solar panel efficiency (as a decimal): "))
    solar_irradiance = float(input("Enter solar irradiance in Watts per square meter: "))

    # Adjust motor power based on load
    adjusted_motor_power = motor_power * motor_load_percentage / 100

    # Calculate and display necessary solar panel size
    panel_size, required_power = calculate_solar_panel_size(adjusted_motor_power, motor_efficiency, panel_efficiency,
                                                            solar_irradiance)
    print(f"\nRequired solar panel area: {panel_size:.2f} square meters")

    max_output = float(input("Enter your solar panel output rating: "))
    panel_efficiency = float(input("Enter your solar panel efficiency (as a decimal): "))
    # Calculate and display solar panel output at different angles
    outputs = solar_panel_output_at_angles(max_output)
    print("\nSolar Panel Power Output at Different Angles:")
    for angle, output in outputs.items():
        if output >= required_power:
            print(f"Angle {angle}°: {output:.2f} W")
        else:
            print(f"Angle {angle}°: {output:.2f} W", " : Maximum angle for functioning motor.")
            break

    # Plot the solar panel output
    plot_solar_panel_output_interactive(outputs)
    # Calculate and display the maximum angle
    motor_min_power = adjusted_motor_power  # Use the adjusted motor power

    max_angle = power_output_at_angles(motor_min_power, max_output, panel_efficiency)
    print(f"\nMaximum angle before the motor won't turn: {max_angle}°")


if __name__ == "__main__":
    main()
