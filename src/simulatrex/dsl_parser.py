from simulatrex.agents.generative_agent import GenerativeAgent
from simulatrex.simulation import Simulation
from simulatrex.environment import Environment
from ply import lex, yacc

# List of token names. This is always required
tokens = (
    "AGENT",
    "ENVIRONMENT",
    "SIMULATION",
    "IDENTIFIER",
    "NUMBER",
    "ATTRIBUTES",
    "ENTITIES",
    "EPOCHS",
    "INTERACTIONS",
    "COLON",
)

# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Additional rule for ignoring newlines and commas
t_ignore_NEWLINE = r"\n+"
t_ignore_COMMA = r","


# Regular expression rule with some action code
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)  # Convert string to integer
    return t


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def t_COLON(t):
    r"\:"
    return t


# Regular expression rules for complex tokens
def t_AGENT(t):
    r"Agent"
    return t


def t_ENVIRONMENT(t):
    r"Environment"
    return t


def t_SIMULATION(t):
    r"Simulation"
    return t


def t_ATTRIBUTES(t):
    r"Attributes"
    return t


def t_ENTITIES(t):
    r"Entities"
    return t


def t_EPOCHS(t):
    r"Epochs"
    return t


def t_INTERACTIONS(t):
    r"Interactions"
    return t


def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    return t


# Build the lexer
lexer = lex.lex(debug=True)


def p_simulation_structure(p):
    """simulation : simulation_entity
    | simulation simulation_entity"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_simulation_entity(p):
    """simulation_entity : agent_definition
    | environment_definition
    | simulation_definition"""
    p[0] = p[1]


def p_agent_definition(p):
    """agent_definition : AGENT COLON IDENTIFIER attributes"""
    agent_identifier = p[3]
    agent_attributes = p[4]
    p[0] = GenerativeAgent(agent_identifier, agent_attributes)


def p_environment_definition(p):
    """environment_definition : ENVIRONMENT COLON IDENTIFIER entities"""
    environment_identifier = p[3]
    environment_entities = p[4]
    p[0] = Environment(environment_identifier, environment_entities)


def p_simulation_definition(p):
    """simulation_definition : SIMULATION COLON IDENTIFIER epochs interactions"""
    simulation_identifier = p[3]
    simulation_epochs = p[4]
    simulation_interactions = p[5]
    p[0] = Simulation(simulation_identifier, simulation_epochs, simulation_interactions)


def p_attributes(p):
    """attributes : ATTRIBUTES COLON list_of_identifiers"""
    p[0] = p[3]


def p_entities(p):
    """entities : ENTITIES COLON list_of_identifiers"""
    p[0] = p[3]


def p_epochs(p):
    """epochs : EPOCHS COLON NUMBER"""
    p[0] = p[3]


def p_interactions(p):
    """interactions : INTERACTIONS COLON list_of_interactions"""
    p[0] = p[3]


def p_list_of_identifiers(p):
    """list_of_identifiers : IDENTIFIER
    | list_of_identifiers IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_list_of_interactions(p):
    """list_of_interactions : interaction
    | list_of_interactions interaction"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_interaction(p):
    """interaction : IDENTIFIER"""
    p[0] = p[1]


def p_error(p):
    if p:
        print(
            f"Syntax error at token {p.type}: '{p.value}', line {p.lineno}, position {p.lexpos}"
        )
    else:
        print("Syntax error at EOF")


parser = yacc.yacc(debug=True)


# Modify the parse_dsl function to return a Simulation instance
def parse_dsl(data):
    try:
        parsed_data = parser.parse(data)
    except Exception as e:
        return None
    if not parsed_data:
        return None  # Early return if parsed_data is empty or None

    simulation = None
    agents = []
    environment = None

    # Assuming parsed_data is a list of items
    for item in parsed_data:
        if isinstance(item, Simulation) and simulation is None:
            simulation = item
        elif isinstance(item, GenerativeAgent):
            agents.append(item)
        elif isinstance(item, Environment) and environment is None:
            environment = item

    if simulation:
        simulation.agents = agents
        simulation.environment = environment
        return simulation
    else:
        return None  # Return None if no Simulation instance was found
